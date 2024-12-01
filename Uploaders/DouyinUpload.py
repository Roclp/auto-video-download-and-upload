# -*- coding: utf-8 -*-
import pathlib
from datetime import datetime

from playwright.async_api import Playwright, async_playwright
import os
import asyncio
import yaml

async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=account_file)
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        try:
            await page.wait_for_selector("div.boards-more h3:text('抖音排行榜')", timeout=5000)  # 等待5秒
            print("[+] 等待5秒 cookie 失效")
            return False
        except:
            print("[+] cookie 有效")
            return True


async def douyin_setup(account_file, handle=False):
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            # Todo alert message
            return False
        print('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        await douyin_cookie_gen(account_file)
    return True


async def douyin_cookie_gen(account_file):
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options)
        # Setup context however you like.
        context = await browser.new_context()  # Pass any options
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto("https://www.douyin.com/")
        await page.pause()
        # 点击调试器的继续，保存cookie
        await context.storage_state(path=account_file)


class DouYinVideo(object):
    def __init__(self, title, file_path,cover_path, tags, publish_date: datetime, account_file):
        self.title = title  # 视频标题
        self.file_path = file_path
        self.cover_path = cover_path
        self.tags = tags
        self.publish_date = publish_date
        self.account_file = account_file
        self.date_format = '%Y年%m月%d日 %H:%M'
        self.local_executable_path = ""  # change me
        self.ua = {
            "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                   "Safari/537.36",
            "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
                   "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
        }

    async def set_schedule_time_douyin(self, page, publish_date):
        # 选择包含特定文本内容的 label 元素
        # label_element = page.locator("label.radio--4Gpx6:has-text('定时发布')")
        # label_element = page.locator("[class^='radio']:has-text('定时发布')")

        label_element = page.locator("xpath=/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[12]/div[2]/div[2]/label[2]")
        await asyncio.sleep(0.3)
        label_element = page.locator(".one-line-pe7juM:nth-child(2)")
        await asyncio.sleep(0.3)
        # 在选中的 label 元素下点击 checkbox
        await label_element.click()
        await asyncio.sleep(0.3)
        publish_date_hour = publish_date.strftime("%Y-%m-%d %H:%M")

        await asyncio.sleep(1)
        await page.locator('.semi-input[placeholder="日期和时间"]').click()
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(str(publish_date_hour))
        await page.keyboard.press("Enter")

        await asyncio.sleep(1)

    async def handle_upload_error(self, page):
        print("视频出错了，重新上传中")
        await page.locator('div.progress-div [class^="upload-btn-input"]').set_input_files(self.file_path)

    async def upload(self, playwright: Playwright) -> None:
        # 使用 Chromium 浏览器启动一个浏览器实例
        headless=True
        if self.local_executable_path:
            browser = await playwright.chromium.launch(channel="chrome",headless=headless, executable_path=self.local_executable_path)
        else:
            browser = await playwright.chromium.launch(channel="chrome",headless=headless)
        # 创建一个浏览器上下文，使用指定的 cookie 文件
        context = await browser.new_context(storage_state=self.account_file, user_agent=self.ua["web"])

        

        # 创建一个新的页面
        page = await context.new_page()

        # if not await cookie_auth(self.account_file):
        #     print('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        #     await douyin_cookie_gen(self.account_file)
        #     print('[+] cookie文件已生成，请重新运行程序')
        #     return

        # print("正在判断账号是否登录")
        # try:
        #     await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        #     await page.locator(".login").click(timeout=1500)
        #     print("未登录，正在跳出")
        # except Exception as e:
        #     # print("出现此error，代表cookie正常反之异常\n", e)
        #     print("账号已登录")
            
        try:
            # 访问指定的 URL
            await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            print('[+]正在上传-------{}.mp4'.format(self.title))
            # 等待页面跳转到指定的 URL，没进入，则自动等待到超时
            print('[-] 正在打开主页...')
            await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload")
            # 点击 "上传视频" 按钮
            # await page.locator(".upload-btn--9eZLd").set_input_files(self.file_path)
            # await page.locator("[name='upload-btn']").set_input_files(self.file_path)
            await page.locator("input[accept='video/*']").set_input_files(self.file_path)
        except Exception as e:
            print('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
            await douyin_cookie_gen(self.account_file)
            print('[+] cookie文件已生成，请重新运行程序')
            self.upload(playwright)


        # 等待页面跳转到指定的 URL
        while True:
            # 判断是是否进入视频发布页面，没进入，则自动等待到超时
            try:
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page")
                break
            except:
                print("  [-] 正在等待进入视频发布页面...")
                await asyncio.sleep(0.1)

        # 填充标题和话题
        # 检查是否存在包含输入框的元素
        # 这里为了避免页面变化，故使用相对位置定位：作品标题父级右侧第一个元素的input子元素
        await asyncio.sleep(1)
        print("  [-] 正在填充标题和话题...")

        # 使用属性选择器定位<input>元素
        # input_locator = page.locator('input[placeholder="好的作品标题可获得更多浏览"]')
        input_locator = page.locator('input[placeholder="填写作品标题，为作品获得更多流量"]')
        # 向<input>元素输入文本
        await input_locator.click()
        await input_locator.type(self.title[0:30])

        # title_container = page.get_by_text('作品标题').locator("..").locator("xpath=following-sibling::div[1]").locator("input")
        # if await title_container.count():
        #     await title_container.fill(self.title[:30])
        #     print("  [-]标题填充完毕")
        # else:
        #     titlecontainer = page.locator(".notranslate")
        #     await titlecontainer.click()
        #     print("clear existing title")
        #     await page.keyboard.press("Backspace")
        #     await page.keyboard.press("Control+KeyA")
        #     await page.keyboard.press("Delete")
        #     print("filling new  title")
        #     await page.keyboard.type(self.title)
        #     await page.keyboard.press("Enter")
        css_selector = ".zone-container"
        for index, tag in enumerate(self.tags, start=1):
            print("正在添加第%s个话题" % index)
            await page.type(css_selector, "#" + tag)
            await page.press(css_selector, "Space")


        
        


        # 选择视频封面
        #await asyncio.sleep(1000000000000000)
        # await page.locator('div.cover-lTOzOo').click()
        await page.locator('div.filter-k_CjvJ').nth(1).click()
        await asyncio.sleep(1)

        # 设置竖封面 semi-button semi-button-primary semi-button-light primary-RstHX_
        await page.locator('.semi-button.semi-button-primary.semi-button-light.primary-RstHX_').click()
        # await asyncio.sleep(10000000)


        # 重选底图 semi-button-content
        await page.locator('.semi-button-content:has-text("重选底图")').click()
        await asyncio.sleep(0.3)
        
     
        # 点击上传封面
        # await page.locator('div.tabItem-BKqlgq:has-text("上传封面")').click()
        # await page.wait_for_selector('.wrap--34lZx div:nth-child(2)');
        # await page.click('.wrap--34lZx div:nth-child(2)');
        

        
        # await page.wait_for_selector('.semi-upload-hidden-input');

        # accept="image/png,image/jpeg,image/jpg,image/bmp,image/webp,image/tif"
        await page.locator('.semi-upload-hidden-input').set_input_files(self.cover_path)
        # await page.locator(".semi-upload-hidden-input").set_input_files(self.cover_path)
        await asyncio.sleep(0.5)
 
        # 完成 confirm-qvC4Vg 小封面完成
        await page.locator('div.confirm-qvC4Vg:has-text("完成")').nth(1).click()

        # 完成 semi-button semi-button-primary semi-button-light primary-RstHX_ 封面编辑完成
        await page.locator('.semi-button.semi-button-primary.semi-button-light.primary-RstHX_').click()

        # await asyncio.sleep(100000000)


        # await page.locator('div.selectItem--2jZ_U:has-text("竖封面")').click()
        # await page.locator('div:has-text("竖封面")').click()
        # await page.locator(f'xpath=/html/body/div[13]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div').click()
        # await page.locator('div.selectItem--2jZ_U:has-text("竖封面")').nth(1).click()
        # await asyncio.sleep(0.5)
        # await page.locator('button.semi-button.semi-button-primary.semi-button-light.finish--3_3_P:nth-child(2)').click()
        
        
        # await page.locator('div.selectItem-rIFAp2:has-text("竖封面")').nth(1).click()
        # await asyncio.sleep(0.5)
        # await page.locator('button.semi-button.semi-button-primary.semi-button-light.finish-Y2Ps_0:nth-child(2)').click()
        

        
        
        
       
        # 更换可见元素
        # await page.locator('div.semi-select span:has-text("输入地理位置")').click()
        # await asyncio.sleep(1)
        # print("clear existing location")
        # await page.keyboard.press("Backspace")
        # await page.keyboard.press("Control+KeyA")
        # await page.keyboard.press("Delete")
        # await page.keyboard.type("广东市")
        # await asyncio.sleep(1)
        # await page.locator('div[role="listbox"] [role="option"]').first.click()

        # 頭條/西瓜
        third_part_element = '[class^="info"] > [class^="first-part"] div div.semi-switch'
        # 定位是否有第三方平台
        if await page.locator(third_part_element).count():
            # 检测是否是已选中状态
            if 'semi-switch-checked' not in await page.eval_on_selector(third_part_element, 'div => div.className'):
                # await page.locator(third_part_element).locator('input.semi-switch-native-control').click()
                pass
            else:
                await page.locator(third_part_element).locator('input.semi-switch-native-control').click()

        if self.publish_date != 0:
            await self.set_schedule_time_douyin(page, self.publish_date)


        while True:
            # 判断重新上传按钮是否存在，如果不存在，代表视频正在上传，则等待
            try:
                #  新版：定位重新上传
                number = await page.locator('div:has-text("预览封面/标题")').count()
                if number > 0:
                    print("  [-]视频上传完毕")
                    break
                else:
                    print("  [-] 正在上传视频中...")
                    await asyncio.sleep(2)

                    if await page.locator('div.progress-div > div:has-text("上传失败")').count():
                        print("  [-] 发现上传出错了...")
                        await self.handle_upload_error(page)
            except:
                print("  [-] 正在上传视频中...")
                await asyncio.sleep(0.2)
                
        # 星图任务和游戏手柄无法同时选择

        # 选择星图任务
        # await page.locator('.star-btn-poAMX1').click()
        # await page.locator('.order-name-ZRQUeW').click()
        # await page.locator('.my-btn-R4WFto:nth-child(2)').click()

        # 挂载游戏手柄
        # await page.locator('.semi-select-selection:nth-child(2) .semi-select-selection-text').click()
        # input_locator = page.locator('.semi-select-input > .semi-input')
        # # 输入游戏名称
        # await input_locator.click()
        # await page.keyboard.type("我的世界")

        # await page.locator('.anchor-game-option-C_pqR6:nth-child(1) .anchor-game-option__rt-XhhIKL').click()


        # 添加挑战贴纸
        # await page.locator('semi-select-selection-text.semi-select-selection-placeholder').click()

        # await asyncio.sleep(100)
        
        # 判断视频是否发布成功
        while True:
            # 判断视频是否发布成功
            try:
                publish_button = page.get_by_role('button', name="发布", exact=True)
                if await publish_button.count():
                    await publish_button.click()
                # await page.wait_for_url("https://creator.douyin.com/creator-micro/content/manage",
                #                         timeout=1500)  # 如果自动跳转到作品页面，则代表发布成功
                print("  [-]视频发布成功")
                break
            except:
                print("  [-] 视频正在发布中...")
                await page.screenshot(full_page=True)
                await asyncio.sleep(0.5)

        await context.storage_state(path=self.account_file)  # 保存cookie
        print('  [-]cookie更新完毕！')
        await asyncio.sleep(2)  # 这里延迟是为了方便眼睛直观的观看
        # 关闭浏览器上下文和浏览器实例
        await context.close()
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)

def getFileNames(file_path):
    videoFile = []
    files = os.listdir(file_path)
    files = sorted(files,  key=lambda x: os.path.getctime(os.path.join(file_path, x)))
    for i in range(len(files)):
        if (files[i][-4:] == "webm" or files[i][-4:] == ".mkv" or files[i][-4:] == ".mp4"):
            videoFile.append(files[i])
    return videoFile

# account_file = "account.json"
# asyncio.run(douyin_cookie_gen(account_file))
# cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
# app = DouYinVideo('title', 'file', 'tags', 'publish_datetimes[index]', r'D:\desktop\myself\cookie\cookie_13638750465.json')
if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    fullpath = config['path']+config['dir']
    print(fullpath)
    videoFile = getFileNames(fullpath)
    print(f"{fullpath} 文件夹下有 {len(videoFile)} 个视频")
    
    account_file = r'D:\desktop\myself\cookie\cookie_13638750465.json'
    
    # publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    # cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
    
    tags=["我的世界"]
    file= r"D:\desktop\myself\video\我的世界：变成钻石骷髅在MC中生存100天！【第1集】.mp4"
    title="变成钻石骷髅在MC中生存100天"
    cover=r"D:\desktop\myself\videos\image1.png"
    app = DouYinVideo(title, file,cover, tags, 0, account_file)
    asyncio.run(app.main(), debug=False)