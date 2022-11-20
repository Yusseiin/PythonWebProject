#<editor-fold desc="New working sheet">

driver = ""
sheetselected = ""
vehicle = ""
daytoload = ""

async def wsnew(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global driver
    global sheetselected
    user = update.message.from_user
    logger.info("ID: %s is start a NewHour", user.id)
    checkuser = db_user.get(Query().ChatId == str(user.id))
    checkmmf = db_mmf.get(Query().ChatId == str(user.id))
    if str(checkuser) != "None":
        if str(checkmmf) != "None":
            # print("Record gia esistente")
            sUser = checkuser.get("Username")
            sUserLogin = checkmmf.get("Username")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=
            f"Hi {sUser}!\nI'am opening your portal, wait a second",
                                           )
            #driver = openFirefox(False, "http://marweb.marchianisrl.com:8086/")
            driver = openChrome("http://marweb.marchianisrl.com:8086/")
            pwd = checkmmf.get("Pwd")
            pwd = pwd.encode('utf-8')
            sPwd = decPwd(pwd)
            insertTextByID("USERNAME", 0, sUserLogin, driver)
            insertTextByID("PASSWORD", 0, sPwd, driver)
            clickOnID("LOGIN", 0, driver)
            clickOnID("cms:12:link", 0, driver)
            clickOnCSS("#cmd\:13 > a", 0, driver)
            clickOnCSS("#pan\:4\:13\:new", 1, driver)
            clickOnCSS("#pan\:4\:13\:fb > div:nth-child(1) > div:nth-child(1) > div > div > span > button", 1,
                       driver)  # foglio di lavoro
            counter = 0
            asFogliLavoro = ""
            reply_keyboard = []
            for x in range(20):
                Delay = 0
                elements = ""
                xPath = "/html/body/div[8]/table/tbody/tr[" + str(x) + "]"
                if x == 2:
                    Delay = 100
                if x > 1:
                    elements = findsByXpath(xPath, Delay, driver)
                    if elements == "End":
                        break
                    else:
                        asFogliLavoro = asFogliLavoro + str(x) + " - " + elements + "\n--------------\n"
                        counter = counter + 1
                        reply_keyboard.append(str(x))
            reply_keyboard = [reply_keyboard]
            if counter == 0:
                print("You do not have working sheet open.")
                return ConversationHandler.END
            else:
                if counter == 1:
                    sheetselected = str(2)
                    xPath = "/html/body/div[8]/table/tbody/tr[" + str(sheetselected) + "]"
                    clickOnXpath(xPath, 0, driver)
                    await update.message.reply_text(
                        f"You have only 1 working sheet open.\n"
                        f"{asFogliLavoro}"
                        "How many hours do you wanna load?",
                    )
                    return MMFWSVEHICLE
                else:
                    await update.message.reply_text(
                        f"You have this working sheet open.\n"
                        f"{asFogliLavoro}"
                        "What number do you wanna use?",
                        reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select you pokemon?"
                        ),
                    )

                    return MMFWSVEHICLE
        else:
            await update.message.reply_text(
                f"Hi {user.id}! My name is MarfBot.\n"
                "I do not know you\n"
                "Please send /mmfsingup to give me your details.",
            )
            return ConversationHandler.END
    else:
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I do not know you\n"
            "Please send /singup to give me your details.",
        )
        return ConversationHandler.END

async def wsnewvehicles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
        #fiififiifififififi
    if sheetselected != str(2):
        user = update.message.from_user
        logger.info("Number of sheet of %s: %s", user.first_name, update.message.text)
        sheetselected = update.message.text
        # fiififiifififififi
    xPath = "/html/body/div[8]/table/tbody/tr[" + str(sheetselected) + "]"
    clickOnXpath(xPath, 0, driver)
    counter = 0
    clickOnCSS("#pan\:4\:13\:fb > div:nth-child(2) > div:nth-child(3) > div > div > span > button", 1,
               driver)  # mezzo assegnato
    for x in range(20):
        Delay = 0
        elements = ""
        xPath = "/html/body/div[9]/table/tbody/tr[" + str(x) + "]"
        if x == 2:
            Delay = 100
        if x > 1:
            elements = findsByXpath(xPath, Delay, driver)
            if elements == "End":
                break
            else:
                counter = counter + 1
                print(str(x) + " - " + elements)
                keyboard.append(InlineKeyboardButton((elements), callback_data=str(x)))
    keyboard = [keyboard]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a vehicle: ",
                                    reply_markup=reply_markup)
    return MMFWSDAY

async def wsnewday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global vehicle
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    vehicle = update.message.text
    xPath = "/html/body/div[9]/table/tbody/tr[" + str(vehicle) + "]"
    clickOnXpath(xPath, 0, driver)
    logger.info("Vehicle chosen of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Please select a date: ",
                                    reply_markup=telegramcalendar.create_calendar())
    return MMFWSDESCRIPTION

async def wsnewdescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global daytoload
    # print(update.callback_query.data)
    selected, date, year, month = telegramcalendar.process_calendar_selection(update)
    query = update.callback_query
    await query.answer()
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    if selected:
        sSplit = query.data.split(";")
        # sData = sSplit[4]+"/"+sSplit[3]+"/"+sSplit[2]
        sData = date.strftime("%d/%m/%Y")
        daytoload = sData
        logger.info("Day to load: %s", sData)
        await query.edit_message_text(text=f"Ok i will load at {sData}!\nTell me the description you wanna use?", )
        return MMFWSINSERT
    else:
        await query.edit_message_text(text="Please select a date: ",
                                      reply_markup=telegramcalendar.create_calendar(year, month))

async def wsnewinsert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
    global vehicle
    global daytoload
    global description
    global driver
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Number of day of %s: %s", user.first_name, update.message.text)
    description = update.message.text
    checkuser = db_user.get(Query().ChatId == str(user.id))
    sUser = checkuser.get("Username")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
    f"Ok {sUser}!\nI'am loading the new working sheet",
                                   )
    clickOnCSS("#pan\:4\:13\:save", 0, driver)
    sleep(5)
    #closeFirefox(driver)
    closeChrome(driver)
    print("Selenium_END!!")
    await update.message.reply_text(
        f"You hours are correctly load.",
    )
    return ConversationHandler.END

#</editor-fold>