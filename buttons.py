from telegram import KeyboardButton, InlineKeyboardButton

main_menu = [
    [
        KeyboardButton(text="Kod bo'yicha qidirish"),
        KeyboardButton(text="Yil bo'yicha qidirish")
    ],
    [
        KeyboardButton(text="Janr bo'yicha qidirish"),
        KeyboardButton(text="Nomi bo'yicha qidirish")
    ]
]

buttons_for_admin = [
            [KeyboardButton(text="Kino qo'shish"), KeyboardButton(text="Kinoni tahrirlash")],
            [KeyboardButton(text="Kinoni o'chirish"), KeyboardButton(text="Kinolar ro'yxati")]
        ]

back = [[KeyboardButton(text="Bosh menyu")]]
