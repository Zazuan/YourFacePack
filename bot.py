import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import face_recognition
import numpy as np
import cv2
import tempfile

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        await photo_file.download_to_drive(f.name)
        image = face_recognition.load_image_file(f.name)
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) != 1:
            await update.message.reply_text("Пожалуйста, отправьте фото с ОДНИМ лицом.")
            return

        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        face_image_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)

        face_path = f.name.replace(".jpg", "_face.jpg")
        cv2.imwrite(face_path, face_image_bgr)

        await update.message.reply_photo(photo=open(face_path, 'rb'), caption="Лицо распознано!")

        os.remove(f.name)
        os.remove(face_path)

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
