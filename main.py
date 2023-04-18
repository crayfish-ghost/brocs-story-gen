# -*- coding: utf-8 -*-
import openai
import os, random, time, datetime, json, logging
from configparser import ConfigParser

# 設定ファイル読み込み
BASE_DIR = os.path.abspath( os.path.dirname(__file__) )
config = ConfigParser()
config.read(BASE_DIR + "/config.ini", encoding='utf-8')

# 設定値読み込み
openai.api_key            = config.get('gpt','api_key')
GPT_MODEL                 = config.get('gpt','model')
GPT_TIMEOUT               = config.get('gpt','timeout')
GPT_SYSTEM_PROMPT         = config.get('gpt','system_prompt')
GPT_TEMPERATURE_HIGH      = float( config.get('gpt','temperature_high') )
GPT_TEMPERATURE_NORMAL    = float( config.get('gpt','temperature_normal') )
STEP1_CONTENT_CHAR_LENGTH = int( config.get('prompt','step1_content_char_length') )
STEP1_CONTENT_NUM         = int( config.get('prompt','step1_content_num') )
DEFAULT_TITLES            = json.loads( config.get('prompt','default_titles') )

# 各種ディレクトリ設定
PROMPTS_DIR       = BASE_DIR + "/prompts"
LOG_DIR           = BASE_DIR + "/logs"
PROMPT_STEP1_FILE = PROMPTS_DIR + "/step1.txt"
PROMPT_STEP2_FILE = PROMPTS_DIR + "/step2.txt"

def main():
    # ログ設定
    log_constructor( LOG_DIR )

    logging.info("start processing")
    # gptとのやりとり1回目
    # 生成したいコンテンツのタイトル案を複数生成する
    # 直接コンテンツを生成すると中身がワンパターンになるため、最初にタイトル案を複数作らせて内容に幅を持たせる
    logging.info("start gpt step1.")
    step1_message = create_gpt_message_step1( get_step1_prompt() )
    try:
        step1_response = get_gpt_response(step1_message, GPT_TEMPERATURE_HIGH )
        logging.info("gpt step1 got responses: " + step1_response)
    except Exception as e:
        exception_name = type(e).__name__
        exception_message = str(e)
        logging.warn( exception_name + ": " + exception_message )

    # タイトル案が正しく生成されていなさそうであれば、念のため用意しておいたデフォルトタイトルを利用
    if isok_step1(step1_response):
        content_titles = step1_response.split("\n")
    else:
        content_titles = DEFAULT_TITLES
        logging.info("use default titles.")

    target_title = random.choice(content_titles)
    logging.info("selected step1 title: " + target_title)
    logging.info("start gpt step2.")
    # gptとのやりとり2回目
    # タイトル案からランダムに選んでタイトルに即したテキストコンテンツを生成
    step2_message = create_gpt_message_step2( step1_message, step1_response, get_step2_prompt( target_title ) )
    try:
        step2_response = get_gpt_response( step2_message, GPT_TEMPERATURE_NORMAL )
        logging.info("gpt step2 got responses." + step2_response)
    except Exception as e:
        exception_name = type(e).__name__
        exception_message = str(e)
        logging.error( exception_name + ": " + exception_message )
        exit(255)

    # 生成したコンテンツを表示
    print(step2_response.replace("\n\n","\n"))
    logging.info("gpt step2 succeeded.")

    exit(0)


# GPTとのやりとり1回目のpromptを作成
def get_step1_prompt():
    prompt_file =open( PROMPT_STEP1_FILE , 'r')
    prompt = prompt_file.read()
    prompt = prompt.replace('__CONTENT_CHAR_LENGTH__', str(STEP1_CONTENT_CHAR_LENGTH) )
    prompt = prompt.replace('__CONTENT_NUM__', str(STEP1_CONTENT_NUM) )
    #ランダムでニュースコンテンツに限定する
    prompt = prompt.replace('__NEWS_OR_NOT__', random.choice( ['ニュース', ''] ) )
    return prompt

# GPTとのやりとり1回目のmessageを作成
def create_gpt_message_step1 (prompt):
    message = [
        {"role": "system", "content": GPT_SYSTEM_PROMPT },
        {"role": "user", "content": prompt }
    ]
    return message


# GPTとのやりとり2回目のpromptを作成
def get_step2_prompt(content_title):
    prompt_file =open( PROMPT_STEP2_FILE , 'r')
    prompt = prompt_file.read()
    #print("対象: " + random_title) #debug
    return prompt.replace('__CONTENT_TITLE__', content_title )

# GPTとのやりとり2回目のmessageを作成
def create_gpt_message_step2 (before_message, before_response, prompt):
    message = before_message
    message.append( { "role": "assistant", "content": before_response } )
    message.append( { "role": "user", "content": prompt } )
    return message


# chatGPTのAPIとのやりとり
def get_gpt_response(message, tpr):
    response = openai.ChatCompletion.create(
        model       = GPT_MODEL ,
        temperature = tpr ,
        messages    = message ,
        timeout     = GPT_TIMEOUT
    )
    return response['choices'][0]['message']['content']


# step1で生成したタイトル案が求めた形式になっているかどうかのチェック
def isok_step1 ( response ):
    # nullはだめ
    if response is None:  # nullはだめ
        logging.warn("gpt step1 response is null.")
        return False
    # 回答が空もだめ
    elif response == '':  # 返答が空もだめ
        logging.warn("gpt step1 response is empty.")
        return False
    # 作ったタイトル数が設定値と違う場合もだめ
    elif len( response.split("\n") ) != STEP1_CONTENT_NUM: 
        logging.warn("gpt step1 response is invalid.")
        return False

    return True

def log_constructor( dir ):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
                        filename=dir + "/processing.log")
    return

if __name__ == "__main__":
    main()
