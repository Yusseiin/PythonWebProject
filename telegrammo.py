from telegram import __version__ as TG_VER
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, \
    TypeHandler, ApplicationHandlerStop, CallbackQueryHandler
from hideme import *
#from tesseracto import *
from seleniummo import *
from tinydb import TinyDB, Query
import pathlib
import logging
import telegramcalendar

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 4):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

#<editor-fold desc="Initialize directory">

# Start DB
currentpath = str(pathlib.Path(__file__).parent.resolve())
new_dir_name = "Resource"
new_dir = pathlib.Path(currentpath, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
new_dir_name = "db"
new_dir = pathlib.Path(new_dir, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
db_user = TinyDB(str(new_dir) + "/db_user.json")
db_mmf = TinyDB(str(new_dir) + "/db_mmf.json")
db_one = TinyDB(str(new_dir) + "/db_one.json")

# Start Directory
new_dir_name = "Resource"
new_dir = pathlib.Path(currentpath, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
new_dir_name = "Image"
new_dir = pathlib.Path(new_dir, new_dir_name)
new_dir.mkdir(parents=True, exist_ok=True)
image_default_directory = str(new_dir)

#</editor-fold>

#<editor-fold desc="Logging">
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

#</editor-fold>

#<editor-fold desc="Handler">

USERNAME, REALNAME, SURNAME, EMAIL, TELEPHONE = range(5)

MMFUSERNAME, MMFPASSWORD = range(2)

ONEUSERNAME, ONEPASSWORD = range(2)

SPESA, SPESA_TYPE, PHOTO = range(3)

MMFWSDAY, MMFWSVEHICLE, MMFWSDESCRIPTION, MMFWSINSERT = range(4)

MMFNEWHOUR, MMFDAYHOUR, MMFINSERTHOUR, MMFDESCRIPTION = range(4)

MMFCHECKHOUR = range(1)

#</editor-fold>

#<editor-fold desc="Global">

SPECIAL_USERS = [184646691, 1393622277, 1088409675, 2060956130, 5083998593]  # Allows users

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.from_user.id in SPECIAL_USERS:
            user = update.message.from_user
            # logger.info("ID: %s is registered", user.id)

            pass
        else:
            user = update.message.from_user
            logger.info("ID: %s is not enabled", user.id)
            await update.effective_message.reply_text(
                "Hey! You are not allowed to use me!"
            )
            raise ApplicationHandlerStop
    except AttributeError:
        print("No attribute")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s has started", user.first_name)
    await update.message.reply_text(
        f"Hi {user.id}! My name is MarfBot.\n"
        "I am a powerful tool and i am here to make your life easier\n"
        "Jessica won't never ask you again to fix your working sheet :)\n"
        "Please send a /signup to continue",
    )
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s ask for help", user.first_name)
    await update.message.reply_text(
        f"Hi {user.first_name}! My name is MarfBot.\n"
        "Here you have a list of all command that you can use\n"
        "/singup to register yourself to me\n"
        "/mmfsignup to register yourself for hours\n"
        "/onesingup to register yourself for onedrive\n"
        "/hnew to load new hours\n"
        "/hcheck to check the loaded hours\n"
        "more function will come soon :)"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    global driver
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    closeChrome(driver)
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="Sing up">

async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("ID: %s is start a registration", user.id)
    check = db_user.get(Query().ChatId == str(user.id))
    if str(check) != "None":
        print("Record gia esistente")
        name = check.get("Username")
        await update.message.reply_text(
            f"Hi {name}!\nI know you already, are you here for the 'MarfEnergy' ? :)",
        )
        return ConversationHandler.END
    else:
        db_user.insert(
            {
                "Username": "Username",
                "Realname": "Realname",
                "Surname": "Surname",
                "Email": "Email",
                "Telephone": "Telephone",
                "ChatId": str(user.id),
            }
        )
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I will ask you some question so we can know eachother better\n"
            "Send /cancel to stop talking to me.\n"
            "How can i call you?",
        )
    return USERNAME

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_user.update({"Username": textReceived}, Query().ChatId == str(user.id))
    logger.info("Username of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Nice to meet you {textReceived}\n" "What is your real name?",
    )
    return REALNAME

async def realname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_user.update({"Realname": textReceived}, Query().ChatId == str(user.id))
    logger.info("Realname of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Oooh i see {textReceived}\n" "and your surname?",
    )
    return SURNAME

async def surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_user.update({"Surname": textReceived}, Query().ChatId == str(user.id))
    logger.info("Surname of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Thats nice Mr/Ms/Other {textReceived}\n" "Give me an email to contact you?",
    )
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_user.update({"Email": textReceived}, Query().ChatId == str(user.id))
    logger.info("Email of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Muahahah spam incoming to \n{textReceived}\n"
        "And do you have a telephone number?",
    )
    return TELEPHONE

async def telephone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_user.update({"Telephone": textReceived}, Query().ChatId == str(user.id))
    logger.info("Telephone of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        "Do you want to move to 'MarfEnergy'?\n"
        "It is good, only 99,99$/Khw\n."
        f"I will call {textReceived}"
        " later for that, but for now is it all!\nI hope we can talk again some day.",
    )
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="MMF Sing up">

async def mmfsignup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("ID: %s is start a Mmfregistration", user.id)
    check = db_mmf.get(Query().ChatId == str(user.id))
    if str(check) != "None":
        print("Record gia esistente")
        name = check.get("Username")
        await update.message.reply_text(
            f"Hi {name}!\nI know you already, are you here for the 'MarfEnergy' ? :)",
        )
        return ConversationHandler.END
    else:
        db_mmf.insert(
            {
                "Username": "Username",
                "Pwd": "Pwd",
                "ChatId": str(user.id),
            }
        )
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I will ask you some question so i manage your hours\n"
            "Send /cancel to stop talking to me.\n"
            "Give me the login username?\n"
            "(It should be your email address)",
        )
    return MMFUSERNAME

async def mmfusername(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_mmf.update({"Username": textReceived}, Query().ChatId == str(user.id))
    logger.info("Username of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Login is {textReceived}\n" "And for the login password?\n"
        "N.B. This will be stored encrypted",
    )
    return MMFPASSWORD

async def mmfpassword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    pwd = encPwd(textReceived)
    pwd = pwd.decode('utf-8')
    db_mmf.update({"Pwd": str(pwd)}, Query().ChatId == str(user.id))
    logger.info("Password of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Thanks, so i will use {textReceived} as password\n"
        f"This will be encrypted as:\n{pwd}\n"
        "For now that is all!",
    )
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="One Sing up">

async def onesignup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("ID: %s is start a Oneregistration", user.id)
    check = db_one.get(Query().ChatId == str(user.id))
    if str(check) != "None":
        print("Record gia esistente")
        name = check.get("Username")
        await update.message.reply_text(
            f"Hi {name}!\nI know you already, are you here for the 'MarfEnergy' ? :)",
        )
        return ConversationHandler.END
    else:
        db_one.insert(
            {
                "Username": "Username",
                "Pwd": "Pwd",
                "ChatId": str(user.id),
            }
        )
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I will ask you some question so i manage your hours\n"
            "Send /cancel to stop talking to me.\n"
            "Give me your username?",
        )
    return ONEUSERNAME

async def oneusername(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    db_one.update({"Username": textReceived}, Query().ChatId == str(user.id))
    logger.info("Username of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"One User Login is {textReceived}\n" "And for the password?\n"
        "N.B. This will be stored encrypted",
    )
    return ONEPASSWORD

async def onepassword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    textReceived = update.message.text
    pwd = encPwd(textReceived)
    pwd = pwd.decode('utf-8')
    db_one.update({"Pwd": str(pwd)}, Query().ChatId == str(user.id))
    logger.info("Username of %s: %s", user.first_name, textReceived)
    await update.message.reply_text(
        f"Thanks, so i will use {textReceived} as password\n"
        f"This will be encrypted as:\n{pwd}\n"
        "For now that is all!",
    )
    return ConversationHandler.END

#</editor-fold>

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
            driver = openFirefox(False, "http://marweb.marchianisrl.com:8086/")
            #driver = openChrome("http://marweb.marchianisrl.com:8086/")
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
                        "Searching for vehicles",
                    )
                    xPath = "/html/body/div[8]/table/tbody/tr[" + str(sheetselected) + "]"
                    clickOnXpath(xPath, 0, driver)
                    counter = 0
                    sleep(1)
                    clickOnCSS("#pan\:4\:13\:fb > div:nth-child(2) > div:nth-child(3) > div > div > span > button", 1,
                               driver)  # mezzo assegnato
                    keyboard = []
                    row=[]
                    for x in range(40):
                        Delay = 0
                        elements = ""
                        xPath = "/html/body/div[9]/table/tbody/tr[" + str(x) + "]"
                        if x == 2:
                            Delay = 100
                        if x > 1:
                            elements = findsByXpath(xPath, Delay, driver)
                            if elements == "End":
                                keyboard.append(row)
                                break
                            else:
                                counter = counter + 1
                                print(str(x) + " - " + elements)
                                elements = elements.replace('RENAULT ', '')
                                row.append(InlineKeyboardButton(elements, callback_data=str(x)))
                                if (counter % 2)==0:
                                    keyboard.append(row)
                                    row = []
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Please select a vehicle: ",
                                                    reply_markup=reply_markup)
                    return MMFWSDAY
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
    user = update.message.from_user
    logger.info("Number of sheet of %s: %s", user.first_name, update.message.text)
    sheetselected = update.message.text
    xPath = "/html/body/div[8]/table/tbody/tr[" + str(sheetselected) + "]"
    sleep(1)
    clickOnXpath(xPath, 0, driver)
    counter = 0
    clickOnCSS("#pan\:4\:13\:fb > div:nth-child(2) > div:nth-child(3) > div > div > span > button", 1,
               driver)  # mezzo assegnato
    keyboard=[]
    row=[]
    for x in range(40):
        Delay = 0
        elements = ""
        xPath = "/html/body/div[9]/table/tbody/tr[" + str(x) + "]"
        if x == 2:
            Delay = 100
        if x > 1:
            elements = findsByXpath(xPath, Delay, driver)
            if elements == "End":
                keyboard.append(row)
                break
            else:
                counter = counter + 1
                print(str(x) + " - " + elements)
                elements = elements.replace('RENAULT ', '')
                row.append(InlineKeyboardButton(elements, callback_data=str(x)))
                if (counter % 2) == 0:
                    keyboard.append(row)
                    row = []
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a vehicle: ",
                                    reply_markup=reply_markup)
    return MMFWSDAY

async def wsnewday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global vehicle
    """Stores the selected gender and asks for a photo."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    print(query)
    vehicle = query.data
    xPath = "/html/body/div[9]/table/tbody/tr[" + str(vehicle) + "]"
    clickOnXpath(xPath, 0, driver)
    logger.info("Vehicle to load: %s", vehicle)
    await query.edit_message_text(text=f"Selected option: {query.data}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please select a date: ",
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
        insertDateByCSS("#fld\:4\:4\:13\:fv", 1,
                        "#pan\:4\:13\:fb > div:nth-child(2) > div:nth-child(2) > div > div > span > button", daytoload,
                        driver)
        await query.edit_message_text(text=f"Ok i will load at {sData}!\nTell me the description you wanna use?", )
        return MMFWSINSERT
    else:
        await query.edit_message_text(text="Please select a date: ",
                                      reply_markup=telegramcalendar.create_calendar(year, month))

async def wsnewinsert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
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
    insertTextByCSS("#fld\:8\:4\:13\:fv", 1, description, driver)
    clickOnCSS("#pan\:4\:13\:save", 0, driver)
    sleep(2)
    #closeFirefox(driver)
    closeChrome(driver)
    print("Selenium_END!!")
    await update.message.reply_text(
        f"You hours are correctly load.",
    )
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="New hour">

driver = ""
sheetselected = ""
hourstoload = ""
daytoload = ""
description = ""

async def hnew(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            driver = openFirefox(False, "http://marweb.marchianisrl.com:8086/")
            #driver = openChrome("http://marweb.marchianisrl.com:8086/")
            pwd = checkmmf.get("Pwd")
            pwd = pwd.encode('utf-8')
            sPwd = decPwd(pwd)
            insertTextByID("USERNAME", 0, sUserLogin, driver)
            insertTextByID("PASSWORD", 0, sPwd, driver)
            clickOnID("LOGIN", 0, driver)
            clickOnID("cms:12:link", 0, driver)
            clickOnCSS("#cmd\:13 > a", 0, driver)
            asFogliLavoro = ""
            reply_keyboard = []
            counter = 0
            for x in range(20):
                # sPathFoglioLavoro="fld:0:4:13:lv"+str(x)
                sPathData = "fld:4:4:13:lv" + str(x)
                sPathDescrizione = "fld:6:4:13:lv" + str(x)
                # sFoglioLavoro = findsByID(sPathFoglioLavoro,1,driver)
                nDelay = 0
                if x == 0:
                    nDelay = 10
                sData = findsByID(sPathData, nDelay, driver)
                if x != 0:
                    asFogliLavoro = asFogliLavoro + "\n"
                if sData != "End":
                    sDescrizione = findsByID(sPathDescrizione, 0, driver)
                    asFogliLavoro = asFogliLavoro + str(x) + "\n" + sData + "\n" + sDescrizione + "\n--------------\n"
                    reply_keyboard.append(str(x))
                    if sDescrizione != "":
                        counter = counter + 1
                    # print(reply_keyboard)
                else:
                    # closeFirefox(driver)
                    break
            reply_keyboard = [reply_keyboard]
            # print(reply_keyboard)
            if counter == 0:
                print("You do not have working sheet open.")
                return ConversationHandler.END
            else:
                if counter == 1:
                    sheetselected = str(0)
                    await update.message.reply_text(
                        f"You have only 1 working sheet open.\n"
                        f"{asFogliLavoro}"
                        "How many hours do you wanna load?",
                    )
                    return MMFDAYHOUR
                else:
                    await update.message.reply_text(
                        f"You have this working sheet open.\n"
                        f"{asFogliLavoro}"
                        "What number do you wanna use?",
                        reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select you pokemon?"
                        ),
                    )

                    return MMFNEWHOUR
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

async def howmanyhour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Number of sheet of %s: %s", user.first_name, update.message.text)
    sheetselected = update.message.text
    await update.message.reply_text(
        f"I see you choose the {update.message.text} pokemon!\n"
        "How many hours do you wanna load?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MMFDAYHOUR

async def whatdayhour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hourstoload
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    hourstoload = update.message.text
    logger.info("Number of hours of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Please select a date: ",
                                    reply_markup=telegramcalendar.create_calendar())
    return MMFDESCRIPTION

async def mmfdescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global daytoload
    """Stores the selected gender and asks for a photo."""
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
        return MMFINSERTHOUR
    else:
        await query.edit_message_text(text="Please select a date: ",
                                      reply_markup=telegramcalendar.create_calendar(year, month))

async def inserthour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
    global hourstoload
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
    f"Ok {sUser}!\nI'am loading the new hour",
                                   )
    checkmmf = db_mmf.get(Query().ChatId == str(user.id))
    # driver = openFirefox(False,"http://marweb.marchianisrl.com:8086/")
    # driver = openChrome("http://marweb.marchianisrl.com:8086/")
    sUserLogin = checkmmf.get("Username")
    pwd = checkmmf.get("Pwd")
    pwd = pwd.encode('utf-8')
    sPwd = decPwd(pwd)
    """ insertTextByID("USERNAME",0,sUserLogin,driver)
    insertTextByID("PASSWORD",0,sPwd,driver)
    clickOnID("LOGIN",0,driver)
    clickOnID("cms:12:link",0,driver)
    clickOnCSS("#cmd\:13 > a",0,driver) """
    sSheetSelected = "fld:4:4:13:lv" + sheetselected
    clickOnID(sSheetSelected, 0, driver)
    clickOnCSS("#pan\:5\:13\:new", 1, driver)
    insertDateByCSS("#fld\:2\:5\:13\:fv", 1,
                    "#pan\:5\:13\:fb > div:nth-child(1) > div:nth-child(1) > div > div > span > button", daytoload,
                    driver)
    #print(daytoload)
    insertTextByCSS("#fld\:3\:5\:13\:fv", 1, description, driver)
    insertTextByCSS("#fld\:4\:5\:13\:fv", 1, hourstoload, driver)
    clickOnCSS("#pan\:5\:13\:save", 0, driver)
    clickOnCSS("#pan\:5\:13\:save", 0, driver)
    sleep(5)
    #closeFirefox(driver)
    closeChrome(driver)
    print("Selenium_END!!")
    await update.message.reply_text(
        f"You hours are correctly load.",
    )
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="Check hour">

async def hcheck(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global driver
    global sheetselected
    user = update.message.from_user
    logger.info("ID: %s is start a CheckHour", user.id)
    checkuser = db_user.get(Query().ChatId == str(user.id))
    checkmmf = db_mmf.get(Query().ChatId == str(user.id))
    if str(checkuser) != "None":
        if str(checkmmf) != "None":
            sUser = checkuser.get("Username")
            sUserLogin = checkmmf.get("Username")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=
            f"Hi {sUser}!\nI'am opening your portal, wait a second",
                                           )
            driver = openFirefox(False, "http://marweb.marchianisrl.com:8086/")
            #driver = openChrome("http://marweb.marchianisrl.com:8086/")
            pwd = checkmmf.get("Pwd")
            pwd = pwd.encode('utf-8')
            sPwd = decPwd(pwd)
            insertTextByID("USERNAME", 0, sUserLogin, driver)
            insertTextByID("PASSWORD", 0, sPwd, driver)
            clickOnID("LOGIN", 0, driver)
            clickOnID("cms:12:link", 0, driver)
            clickOnCSS("#cmd\:13 > a", 0, driver)
            asFogliLavoro = ""
            reply_keyboard = []
            counter = 0
            for x in range(20):
                sPathData = "fld:4:4:13:lv" + str(x)
                sPathDescrizione = "fld:6:4:13:lv" + str(x)
                nDelay = 0
                if x == 0:
                    nDelay = 10
                sData = findsByID(sPathData, nDelay, driver)
                if x != 0:
                    asFogliLavoro = asFogliLavoro + "\n"
                if sData != "End":
                    sDescrizione = findsByID(sPathDescrizione, 0, driver)
                    asFogliLavoro = asFogliLavoro + str(x) + "\n" + sData + "\n" + sDescrizione + "\n--------------\n"
                    reply_keyboard.append(str(x))
                    if sDescrizione != "":
                        counter = counter + 1
                else:
                    break
            reply_keyboard = [reply_keyboard]
            if counter == 0:
                print("You do not have working sheet open.")
                return ConversationHandler.END
            else:
                if counter == 1:
                    sheetselected = str(0)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=
                        f"You have only 1 working sheet open.\n"
                        f"{asFogliLavoro}"
                        "I'am gonna check the hours loaded",
                    )
                    sSheetSelected = "fld:6:4:13:lv" + str(sheetselected)
                    clickOnID(sSheetSelected, 0, driver)
                    counter = 0
                    asFogliLavoro = ""
                    for x in range(20):
                        sPathData = "fld:2:5:13:lv" + str(x)
                        sPathDescrizione = "fld:3:5:13:lv" + str(x)
                        sPathOreLavorate = "fld:4:5:13:lv" + str(x)
                        sPathOreViaggio = "fld:5:5:13:lv" + str(x)
                        sPathKm = "fld:6:5:13:lv" + str(x)
                        nDelay = 0
                        if x == 0:
                            nDelay = 0
                        sData = findsByID(sPathData, nDelay, driver)
                        if x != 0:
                            asFogliLavoro = asFogliLavoro
                        if sData != "End":
                            sDescrizione = findsByID(sPathDescrizione, 0, driver)
                            sOreLavorate = findsByID(sPathOreLavorate, 0, driver)
                            sOreViaggio = findsByID(sPathOreViaggio, 0, driver)
                            sKm = findsByID(sPathKm, 0, driver)
                            asFogliLavoro = asFogliLavoro + sData + " - " + sDescrizione + \
                                            "\nOre Lavorate: " + sOreLavorate + " - " + "Viaggio: " + sOreViaggio \
                                            + " - " + "Km: " + sKm + " km" + "\n--------------\n"
                            if sDescrizione != "":
                                counter = counter + 1
                        else:
                            break
                    if counter == 0:
                        await update.message.reply_text(
                            "You do not have hours loaded in this sheet",
                            reply_markup=ReplyKeyboardRemove(),
                        )
                    else:
                        await update.message.reply_text(
                            "You have this hours loaded.\n"
                            f"{asFogliLavoro}",
                            reply_markup=ReplyKeyboardRemove(),
                        )
                    closeChrome(driver)
                    return ConversationHandler.END
                else:
                    await update.message.reply_text(
                        f"You have these working sheet open.\n"
                        f"{asFogliLavoro}"
                        "What number do you wanna use?",
                        reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select you pokemon?"
                        ),
                    )
                    return MMFCHECKHOUR
        else:
            await update.message.reply_text(
                f"Hi {user.id}! My name is MarfBot.\n"
                "I do not know you\n"
                "Please send /mmfsignup to give me your details.",
            )
            return ConversationHandler.END
    else:
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I do not know you\n"
            "Please send /signup to give me your details.",
        )
        return ConversationHandler.END

async def checkhour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global sheetselected
    global driver
    user = update.message.from_user
    logger.info("Number of sheet of %s: %s", user.first_name, update.message.text)
    sheetselected = update.message.text
    sSheetSelected = "fld:6:4:13:lv" + str(sheetselected)
    clickOnID(sSheetSelected, 0, driver)
    counter = 0
    asFogliLavoro = ""
    for x in range(20):
        sPathData = "fld:2:5:13:lv" + str(x)
        sPathDescrizione = "fld:3:5:13:lv" + str(x)
        sPathOreLavorate = "fld:4:5:13:lv" + str(x)
        sPathOreViaggio = "fld:5:5:13:lv" + str(x)
        sPathKm = "fld:6:5:13:lv" + str(x)
        nDelay = 0
        if x == 0:
            nDelay = 0
        sData = findsByID(sPathData, nDelay, driver)
        if x != 0:
            asFogliLavoro = asFogliLavoro
        if sData != "End":
            sDescrizione = findsByID(sPathDescrizione, 0, driver)
            sOreLavorate = findsByID(sPathOreLavorate, 0, driver)
            sOreViaggio = findsByID(sPathOreViaggio, 0, driver)
            sKm = findsByID(sPathKm, 0, driver)
            asFogliLavoro = asFogliLavoro + sData + " - " + sDescrizione + \
                            "\nOre Lavorate: " + sOreLavorate + " - " + "Viaggio: " + sOreViaggio \
                            + " - " + "Km: " + sKm + " km" + "\n--------------\n"
            if sDescrizione != "":
                counter = counter + 1
        else:
            break
    if counter == 0:
        await update.message.reply_text(
            "You do not have hours loaded in this sheet",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await update.message.reply_text(
            "You have this hours loaded.\n"
            f"{asFogliLavoro}",
            reply_markup=ReplyKeyboardRemove(),
        )
    closeChrome(driver)
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="Money">

async def spesa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [["Vitto", "Hotel", "Taxi", "Extra"]]

    user = update.message.from_user
    check = db_user.get(Query().ChatId == str(user.id))
    if str(check) != "None":
        name = check.get("Username")
        logger.info("User %s: is sending photo", name)
        await update.message.reply_text(
            f"Welcome back {name}\n" "What type of payment have you done?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Type of payment?"
            ),
        )
        return SPESA_TYPE
    else:
        await update.message.reply_text(
            f"Hi {user.id}! My name is MarfBot.\n"
            "I do not know who you are\n"
            "Please send /registration so i can know you better.\n",
        )
        return ConversationHandler.END

async def spesa_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    global image_default_directory
    global image_directory
    user = update.message.from_user
    logger.info("Type of payment of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        f"I see {update.message.text}!\n"
        "Please send me a photo of the receive",
        reply_markup=ReplyKeyboardRemove(),
    )
    new_dir_name = update.message.text
    new_dir = pathlib.Path(image_default_directory, new_dir_name)
    new_dir.mkdir(parents=True, exist_ok=True)
    image_directory = str(new_dir) + "\\"
    return PHOTO

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global image_default_directory
    global image_directory
    await update.message.reply_text(
        "Image received\n"
        "Wait for the total",
    )
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    aPhoto_name = photo_file.file_path.split("/")
    photo_name = aPhoto_name[len(aPhoto_name) - 1]
    photo_path = image_directory + photo_name
    await photo_file.download(photo_path)
    logger.info("Photo of %s: %s ", user.first_name, photo_name)
    total = "Auto total is not enabled" #getTotal(photo_path)
    await update.message.reply_text(
        f"{total}",
    )
    return ConversationHandler.END

#</editor-fold>

#<editor-fold desc="Main">

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("User: %s is writing: %s", user.first_name, update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("5193004667:AAFVP2LpSEE581TM1dtOOs9k9uKJq_0Oi-I")
        .build()
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    singup_handler = ConversationHandler(
        entry_points=[CommandHandler("signup", signup)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), username)],
            REALNAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), realname)],
            SURNAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), surname)],
            EMAIL: [MessageHandler(filters.TEXT & (~filters.COMMAND), email)],
            TELEPHONE: [MessageHandler(filters.TEXT & (~filters.COMMAND), telephone)],
            # PHOTO: [MessageHandler(filters.PHOTO, image_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    spese_handler = ConversationHandler(
        entry_points=[CommandHandler("spesa", spesa)],
        states={
            SPESA_TYPE: [MessageHandler(filters.TEXT & (~filters.COMMAND), spesa_type)],
            PHOTO: [MessageHandler(filters.PHOTO & (~filters.COMMAND), image_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    mmfsingup_handler = ConversationHandler(
        entry_points=[CommandHandler("mmfsignup", mmfsignup)],
        states={
            MMFUSERNAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), mmfusername)],
            MMFPASSWORD: [MessageHandler(filters.TEXT & (~filters.COMMAND), mmfpassword)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    onesingup_handler = ConversationHandler(
        entry_points=[CommandHandler("onesignup", onesignup)],
        states={
            ONEUSERNAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), oneusername)],
            ONEPASSWORD: [MessageHandler(filters.TEXT & (~filters.COMMAND), onepassword)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    wsnew_handler = ConversationHandler(
        entry_points=[CommandHandler("wsnew", wsnew)],
        states={
            MMFWSVEHICLE: [MessageHandler(filters.TEXT & (~filters.COMMAND), wsnewvehicles)],
            MMFWSDAY: [CallbackQueryHandler(wsnewday)],
            MMFWSDESCRIPTION: [CallbackQueryHandler(wsnewdescription)],
            MMFWSINSERT: [MessageHandler(filters.TEXT & (~filters.COMMAND), wsnewinsert)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    hournew_handler = ConversationHandler(
        entry_points=[CommandHandler("hnew", hnew)],
        states={
            MMFNEWHOUR: [MessageHandler(filters.TEXT & (~filters.COMMAND), howmanyhour)],
            MMFDAYHOUR: [MessageHandler(filters.TEXT & (~filters.COMMAND), whatdayhour)],
            MMFDESCRIPTION: [CallbackQueryHandler(mmfdescription)],
            MMFINSERTHOUR: [MessageHandler(filters.TEXT & (~filters.COMMAND), inserthour)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    hourcheck_handler = ConversationHandler(
        entry_points=[CommandHandler("hcheck", hcheck)],
        states={
            MMFCHECKHOUR: [MessageHandler(filters.TEXT & (~filters.COMMAND), checkhour)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # button_handler = CallbackQueryHandler(button)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)

    handler = TypeHandler(Update, callback)  # Making a handler for the type Update
    application.add_handler(handler, -1)  # Default is 0, so we are giving it a number below 0
    application.add_handler(start_handler, 0)
    application.add_handler(help_handler, 0)
    application.add_handler(singup_handler, 1)
    application.add_handler(mmfsingup_handler, 1)
    application.add_handler(onesingup_handler, 1)
    application.add_handler(wsnew_handler, 1)
    application.add_handler(hournew_handler, 2)
    application.add_handler(hourcheck_handler,2)
    application.add_handler(spese_handler, 2)
    #application.add_handler(echo_handler, 2)
    # application.add_handler(button_handler, 1)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

#</editor-fold>

if __name__ == "__main__":
    main()
