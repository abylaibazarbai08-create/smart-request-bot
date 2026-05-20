from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from asgiref.sync import sync_to_async

from requests_app.models import TelegramUser, Request, Feedback
from bot.keyboards import main_keyboard

router = Router()


class RequestState(StatesGroup):
    waiting_request = State()


class FeedbackState(StatesGroup):
    waiting_feedback = State()


@sync_to_async
def create_or_get_user(message):

    user, created = TelegramUser.objects.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "full_name": message.from_user.full_name
        }
    )

    return user


@sync_to_async
def save_request(user, text):

    Request.objects.create(
        user=user,
        title=text[:30],
        description=text
    )


@sync_to_async
def save_feedback(user, text):

    Feedback.objects.create(
        user=user,
        message=text
    )


@sync_to_async
def get_requests(user):

    return list(
        Request.objects.filter(user=user)
    )


@router.message(Command("start"))
async def start_handler(message: Message):

    user = await create_or_get_user(message)

    await message.answer(
        f"Привет {user.full_name}!\nДобро пожаловать в SmartRequestBot",
        reply_markup=main_keyboard
    )


@router.message(F.text == "Создать заявку")
async def create_request(
        message: Message,
        state: FSMContext
):

    await state.set_state(
        RequestState.waiting_request
    )

    await message.answer(
        "Введите текст заявки:"
    )


@router.message(
    RequestState.waiting_request
)
async def save_request_handler(
        message: Message,
        state: FSMContext
):

    if not message.text.strip():

        await message.answer(
            "Пустой ввод запрещен"
        )

        return

    user = await create_or_get_user(
        message
    )

    await save_request(
        user,
        message.text
    )

    await message.answer(
        "Заявка сохранена ✅"
    )

    await state.clear()


@router.message(F.text == "Мои заявки")
async def show_requests(
        message: Message
):

    user = await create_or_get_user(
        message
    )

    requests = await get_requests(
        user
    )

    if not requests:

        await message.answer(
            "У вас нет заявок"
        )

        return

    text = "Ваши заявки:\n\n"

    for req in requests:

        text += (
            f"{req.title}\n"
            f"Статус: {req.status}\n\n"
        )

    await message.answer(text)


@router.message(F.text == "Оставить отзыв")
async def feedback(
        message: Message,
        state: FSMContext
):

    await state.set_state(
        FeedbackState.waiting_feedback
    )

    await message.answer(
        "Введите отзыв:"
    )


@router.message(
    FeedbackState.waiting_feedback
)
async def feedback_save(
        message: Message,
        state: FSMContext
):

    user = await create_or_get_user(
        message
    )

    await save_feedback(
        user,
        message.text
    )

    await message.answer(
        "Спасибо за отзыв ✅"
    )

    await state.clear()


@router.message()
async def unknown(message: Message):

    await message.answer(
        "Неизвестная команда"
    )