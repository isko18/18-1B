from aiogram import types, Dispatcher
import logging
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from apps.telegram.state.cklient import ClientStates
from apps.telegram.button.cklient import client_keyboard, back_keyboard, cklient_region_keyboard, comment_keyboard, referral_keyboard
from apps.telegram.models import UserCklient, Business
from apps.telegram.management.commands.bot_instance import bot

accepted_requests = set()
searched_requests = set()

async def edit_message_if_different(callback_query: types.CallbackQuery, new_text: str, new_reply_markup):
    current_text = callback_query.message.text
    current_reply_markup = callback_query.message.reply_markup

    if current_text != new_text or current_reply_markup != new_reply_markup:
        await callback_query.message.edit_text(new_text, reply_markup=new_reply_markup)

async def client_start(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info("Команда 'client_start' получена")
    await state.finish()
    await callback_query.answer()
    await edit_message_if_different(
        callback_query,
        "Вы выбрали 'Я клиент'.",
        client_keyboard()
    )
    logging.info('переход')

async def choose_region(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info("Команда 'choose_region' получена")
    await ClientStates.choosing_region.set()
    await callback_query.answer()
    await edit_message_if_different(
        callback_query,
        "Пожалуйста, выберите ваш регион:",
        cklient_region_keyboard()
    )

async def region_selected(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"Регион выбран: {callback_query.data}")
    await state.update_data(region=callback_query.data)
    await ClientStates.entering_date.set()
    await callback_query.answer()
    await edit_message_if_different(
        callback_query,
        "Вы выбрали регион. Пожалуйста, введите дату заезда (дд.мм.гггг):",
        back_keyboard()
    )

async def date_entered(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    region = user_data.get('region')
    date = message.text

    logging.info(f"Дата заезда введена: {date} для региона {region}")

    await state.update_data(date=date)
    await ClientStates.entering_comment.set()
    await message.answer("Пожалуйста, оставьте комментарий:", reply_markup=comment_keyboard())

async def comment_entered(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    region = user_data.get('region')
    date = user_data.get('date')
    comment = message.text

    logging.info(f"Комментарий: {comment}")

    await state.update_data(comment=comment)
    await ClientStates.checking_referral.set()
    await message.answer("Проверка реферальной ссылки...", reply_markup=referral_keyboard())

async def check_referral(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = callback_query.from_user.id

    invited_count = await sync_to_async(UserCklient.objects.filter(referrer_id=user_id).count)()
    required_invites = 1  # Измените здесь количество приглашенных пользователей, если нужно

    logging.info(f"Проверка рефералов: invited_count={invited_count}, required_invites={required_invites}")

    if invited_count >= required_invites:
        await callback_query.message.answer("Вы успешно использовали реферальную ссылку.")
        await state.update_data(invite_check=True)
        await state.finish()
    else:
        invite_link = f"https://t.me/redis_bot?start={user_id}"
        inline_keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Отправить', switch_inline_query=invite_link),
            types.InlineKeyboardButton('Назад', callback_data='go_back')
        )

        await callback_query.message.answer(
            f"Для продолжения вам нужно пригласить хотя бы одного пользователя.\nНужно позвать {invited_count}/{required_invites}",
            reply_markup=inline_keyboard
        )
        await state.set_state(ClientStates.checking_referral)

async def search_action(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    request_id = f"{callback_query.from_user.id}_{user_data.get('region')}_{user_data.get('date')}"
    
    if request_id in searched_requests:
        await callback_query.answer("Вы уже выполнили поиск для этого запроса.", show_alert=True)
        return

    searched_requests.add(request_id)
    
    region = user_data.get('region')
    date = user_data.get('date')
    comment = user_data.get('comment')

    # Отправка запроса бизнес-клиентам
    business_clients = await sync_to_async(list)(Business.objects.filter(region=region, is_active=True).select_related('user'))

    if not business_clients:
        await callback_query.answer("Нет активных объявлений в выбранном регионе.", show_alert=True)
    else:
        for business_client in business_clients:
            accept_decline_keyboard = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton('Принять', callback_data=f'accept_{business_client.id}_{callback_query.from_user.id}'),
                types.InlineKeyboardButton('Отклонить', callback_data=f'decline_{business_client.id}')
            )
            await bot.send_message(
                business_client.user.user_id,  # Убедитесь, что поле user_id у вас правильно указано
                f"Новый запрос от клиента:\n\nРегион: {region}\nДата заезда: {date}\nКомментарий: {comment}",
                reply_markup=accept_decline_keyboard
            )
        await callback_query.answer("Запрос отправлен бизнес-клиентам в вашем регионе.", show_alert=True)
        
        # Добавляем сообщение с предложением поиска в другом районе
        search_other_region_keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Поиск в другом районе', callback_data='search_other_region')
        )
        await bot.send_message(
            callback_query.from_user.id,
            "Ожидайте еще ответы на вашу заявку. Либо попробуйте Поиск в другом районе:",
            reply_markup=search_other_region_keyboard
        )

async def handle_accept(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split('_')
    business_id = int(data[1])
    client_id = int(data[2])
    request_id = f"{callback_query.from_user.id}_{business_id}"

    if request_id in accepted_requests:
        await callback_query.answer("Этот запрос уже был обработан.", show_alert=True)
        return

    accepted_requests.add(request_id)
    
    business_client = await sync_to_async(Business.objects.get)(id=business_id)

    booking_details = (
        f"Регион: {business_client.region}\n"
        f"Пансионат: {business_client.pansionat}\n"
        f"Тип размещения: {business_client.type_accommodation}\n"
        f"Удобства: {business_client.facilities}\n"
        f"Количество мест: {business_client.quantities}\n"
        f"Цена: {business_client.price} USD\n"
        f"Номер телефона: {business_client.phone_number}\n"
    )

    # Отправляем фотографии с описанием
    if business_client.photos:
        photos = business_client.photos.split(',')  # Предполагается, что фотографии хранятся в виде строки, разделенной запятыми
        media = [types.InputMediaPhoto(media=photo) for photo in photos]
        if media:
            media[0].caption = booking_details  # Добавляем описание к первой фотографии
            await bot.send_media_group(client_id, media)
    else:
        await bot.send_message(client_id, booking_details)

    await callback_query.answer("Запрос принят и информация отправлена клиенту.", show_alert=True)

async def handle_decline(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.answer("Запрос был отклонен и сообщение удалено.", show_alert=True)

async def search_other_region(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info("Команда 'search_other_region' получена")
    await choose_region(callback_query, state)

async def go_back(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    logging.info(f"Команда 'go_back' получена, текущее состояние: {current_state}")
    if current_state == ClientStates.checking_referral.state:
        await ClientStates.entering_comment.set()
        await callback_query.answer()
        await edit_message_if_different(
            callback_query,
            "Пожалуйста, оставьте комментарий:",
            comment_keyboard()
        )
    elif current_state == ClientStates.entering_comment.state:
        await ClientStates.entering_date.set()
        await callback_query.answer()
        await edit_message_if_different(
            callback_query,
            "Вы выбрали регион. Пожалуйста, введите дату заезда (дд.мм.гггг):",
            back_keyboard()
        )
    elif current_state == ClientStates.entering_date.state:
        await choose_region(callback_query, state)
    else:
        await client_start(callback_query, state)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(client_start, Text(equals='client_start'), state='*')
    dp.register_callback_query_handler(choose_region, Text(equals='choose_region'), state='*')
    dp.register_callback_query_handler(region_selected, Text(startswith='city_'), state=ClientStates.choosing_region)
    dp.register_callback_query_handler(go_back, Text(equals='go_back'), state='*')
    dp.register_callback_query_handler(go_back, Text(equals='choose_date'), state=ClientStates.entering_comment)
    dp.register_callback_query_handler(check_referral, Text(equals='send_referral'), state=ClientStates.checking_referral)
    dp.register_callback_query_handler(search_action, Text(equals='search'), state='*')
    dp.register_callback_query_handler(search_other_region, Text(equals='search_other_region'), state='*')
    dp.register_callback_query_handler(handle_accept, Text(startswith='accept_'), state='*')
    dp.register_callback_query_handler(handle_decline, Text(startswith='decline_'), state='*')
    dp.register_message_handler(date_entered, state=ClientStates.entering_date)
    dp.register_message_handler(comment_entered, state=ClientStates.entering_comment)