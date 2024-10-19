# -*- coding: utf-8 -*-
import pathlib
from datetime import datetime

from playwright.async_api import Playwright, async_playwright
import os
import asyncio
import yaml

async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=account_file)
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://cp.kuaishou.com/article/publish/video")
        try:
            await page.wait_for_selector(".publish-button", timeout=5000)  # 等待5秒
            print("[+] 等待5秒 cookie 失效")
            return False
        except:
            print("[+] cookie 有效")
            return True
        
async def kuaishou_setup(account_file, handle=False):
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            # Todo alert message
            return False
        print('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        await kuaishou_cookie_gen(account_file)
    return True

async def kuaishou_cookie_gen(account_file):
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
        await page.goto("https://cp.kuaishou.com/article/publish/video")
        await page.pause()
        # 点击调试器的继续，保存cookie
        await context.storage_state(path=account_file)


class KuaiShouVideo(object):
    def __init__(self, title, file_path, cover_path, tags, publish_date: datetime, account_file):
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

    async def set_schedule_time_kuaishou(self, page, publish_date):
        # 选择包含特定文本内容的 label 元素
        label_element = page.locator('label.ant-radio-wrapper:has-text("定时发布")')
        # 在选中的 label 元素下点击 checkbox
        await label_element.click()
        await asyncio.sleep(0.1)
        publish_date_hour = publish_date.strftime("%Y-%m-%d %H:%M:%S")

        await page.locator('input[placeholder="选择日期时间"]').click()

        await page.keyboard.press("Control+KeyA")
   
        await page.keyboard.type(str(publish_date_hour))
        await asyncio.sleep(0.2)
        await page.keyboard.press("Enter")
        await asyncio.sleep(0.2)

        


    async def handle_upload_error(self, page):
        print("视频出错了，重新上传中")
        await page.locator('input[accept="video/*,.mp4,.mov,.flv,.f4v,.webm,.mkv,.rm,.rmvb,.m4v,.3gp,.3g2,.wmv,.avi,.asf,.mpg,.mpeg,.ts"]').set_input_files(self.file_path)


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
        #     await kuaishou_cookie_gen(self.account_file)
        #     print('[+] cookie文件已生成，请重新运行程序')
        #     return

        
        # 等待页面跳转到指定的 URL，没进入，则自动等待到超时
        await asyncio.sleep(1)
        try:
            await page.goto("https://cp.kuaishou.com/article/publish/video")
            await page.wait_for_url("https://cp.kuaishou.com/article/publish/video")
            # 点击 "上传视频" 按钮
            await page.locator('input[accept="video/*,.mp4,.mov,.flv,.f4v,.webm,.mkv,.rm,.rmvb,.m4v,.3gp,.3g2,.wmv,.avi,.asf,.mpg,.mpeg,.ts"]').set_input_files(self.file_path)
        except Exception as e:
            print('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
            await kuaishou_cookie_gen(self.account_file)
            print('[+] cookie文件已生成，请重新运行程序')
            self.upload(playwright)
        
        
        await asyncio.sleep(1)
       
        # 标题 class="_description_10dx2_59" id="work-description-edit"
        # title_selector = "_description_10dx2_59"
        title_selector = f'div[id="work-description-edit"]'
        await page.type(title_selector, self.title)


        await asyncio.sleep(1)
        for tag in self.tags:
            # 点击话题 添加#
            # await page.locator('span:has-text("#话题")').click()
            # 点击话题 “#” _quick-tips_10dx2_353 _quick-tips-topic_10dx2_372
            await page.locator('._quick-tips_10dx2_353._quick-tips-topic_10dx2_372').click()
            await asyncio.sleep(0.1)
            await page.type(title_selector, tag)
            await asyncio.sleep(0.5)
            await page.press(title_selector, "Space")
            await asyncio.sleep(0.1)
            print(f"  [-]添加话题：{tag}")


        # # 选择视频封面
        # # 点击编辑封面
        # await page.locator('button:has-text("编辑封面")').click()
        # # 点击上传封面
        # await page.locator(f'div[id="rc-tabs-2-tab-2"]').click()
        # await asyncio.sleep(1)
        # await page.locator('input[type=file][accept^="image/"]').set_input_files(self.cover_path)
        # # 点击确认
        # await asyncio.sleep(5)
        # # await page.locator(f'xpath=/html/body/div[1]/div[1]/div[1]/main/div/div/div[1]/div/div/haploid-html/haploid-body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/button[1]/span').click()
        # await page.locator('button.ant-btn.ant-btn-primary:has-text("确认")').first.click()
        # await asyncio.sleep(5)
        
        
        
        
        # 所属领域
        # 定位输入框并输入文本
        # 假设您有一个名为 page 的 Playwright 页面对象
        await asyncio.sleep(1)
        elements = await page.locator("input.ant-select-selection-search-input").all()

        # print(elements)


        # 关联变现任务
        # await asyncio.sleep(1)
        # await page.locator('span:has-text("关联变现任务")').click()
        # 定位到特定的span元素
        # span_element = page.locator(
        #     "#joyride-wrapper > div._edit-container_9braw_7 > div:nth-child(2) > "
        #     "div._edit-section_9braw_21._last_9braw_25 > div._edit-section-form_9braw_90 > "
        #     "div.ant-spin-nested-loading > div > div > div > label:nth-child(3) > span:nth-child(2)"
        # )
        # await asyncio.sleep(0.3)
        # # 现在可以使用span_element来执行操作，例如点击
        # await span_element.click(timeout=100000)

        # 获取第一个元素
        # input_locator= elements[0]
        # await input_locator.click()
        
        # #  点击 input_locator 下方10像素的位置
        # # 获取元素的边界框信息
        # box = await input_locator.bounding_box()
        # # 检查边界框是否存在
        # if box:
        #     # 计算点击位置：元素底部向下10像素的位置
        #     click_x = box['x'] + (box['width'] / 2)  # 点击元素中心的水平位置
        #     click_y = box['y'] + box['height'] + 10  # 元素底部向下10像素的垂直位置

        #     # 在计算出的坐标上执行点击操作
        #     await page.mouse.click(click_x, click_y)
        # else:
        #     print("元素没有在页面上，无法获取边界框信息")

        
        # # 获取第一个元素
        # await asyncio.sleep(0.2)
        # input_locator_1= elements[2]
        # await asyncio.sleep(0.2)
        # await input_locator_1.click()
        # # 使用文本选择器定位并点击“影视”分类
        # await page.locator('.ant-select-item-option-content:has-text("游戏")').click()
        # # await page.locator('text=游戏').click()
        # elements = await page.locator("input.ant-select-selection-search-input").all()
        # # 获取第一个元素
        # input_locator_2= elements[3]

        # await input_locator_2.click()
        # # 使用文本选择器定位并点击特定分类
        # await page.locator('text=沙盒游戏').click()





        if self.publish_date != 0:
            await self.set_schedule_time_kuaishou(page, self.publish_date)

        

        while True:
            # 判断重新上传按钮是否存在，如果不存在，代表视频正在上传，则等待
            try:
                #  新版：定位重新上传
                # number = await page.locator('span:has-text("上传成功")').count()
                number = await page.locator('._tab_1ahzu_101:has-text("预览封面")').count()
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
                await asyncio.sleep(2)

        # # 使用模板
        # # 点击使用模板前视频必须已经上传完毕
        # await page.locator('.HtcINKWm2W4-:has-text("使用模板")').click()
        
        # await page.wait_for_selector("._91i17uGkYlI-", state="attached", timeout=30000)  # 等待30秒
        # elements = await page.locator("._91i17uGkYlI-").all()
        # # print(f"elements: {elements}")
        # # 点击第一个元素
        # await asyncio.sleep(1)
        # cnt=len(elements)
        # # 选择第9个模板
        # await elements[cnt-1].click()

        # # 定位<textarea>元素
        # await asyncio.sleep(0.2)
        # # await page.wait_for_selector('textarea.ant-input', state='visible')
        
        # textarea_locator = await page.locator('textarea.ant-input').all()
        # # 清除<textarea>中的现有内容（如果需要）
        # textarea_locator_1=textarea_locator[0]
        # textarea_locator_2=textarea_locator[1]

        # # 使用冒号 ":" 分割字符串，得到一个包含所有部分的列表
        # parts = self.title.split('：')

        # # 提取所需的短语
        # mc=parts[0]  # 提取 "我的世界"
        # bianchen=parts[1].split('在')[0]  # 提取 "变成钻石骷髅"
        # shengcun = '在' + parts[1].split('在')[1].split('【')[0]  # 提取 "MC中生存100天！"
        # dijiji=parts[1].split('【')[1].split('】')[0]  # 提取 "第1集"

        # await asyncio.sleep(0.2)
        # # 向<textarea>元素输入文本
        
        # await textarea_locator_1.click()
        # await page.keyboard.press("Control+KeyA")
        # await asyncio.sleep(0.2)
        # await page.keyboard.press("Delete")
        # # await textarea_locator_1.type(f'{mc}')
        # # await page.keyboard.press("Enter")
        # await textarea_locator_1.type(f'{bianchen}')
        # await page.keyboard.press("Enter")
        # await textarea_locator_1.type(f'{shengcun[:-1]}')

        # await asyncio.sleep(0.1)

        # await textarea_locator_2.click()
        # await page.keyboard.press("Control+KeyA")
        # await asyncio.sleep(0.2)
        # await page.keyboard.press("Delete")
        # await page.keyboard.press("Enter")
        # await page.keyboard.press("Enter")
        # await textarea_locator_2.type(f'{dijiji}')

        # # 点击提交按钮
        # await asyncio.sleep(0.1)
        # await page.locator('button.ant-btn.ant-btn-primary:has-text("提交")').click()


        # 点击开启画质增强 <span>开启</span>
        # await page.locator('span:has-text("点击开启【画质增强】功能，一键提升作品画质")').click()
        # await page.locator('span:has-text("开启")').nth(2).click()
        # asyncio.sleep(10000)


        # # 选择视频封面
        # # 点击编辑封面
        # await page.locator('button:has-text("编辑封面")').click()
        # # 点击上传封面
        # await page.locator(f'div[id="rc-tabs-1-tab-2"]').click() 
        # await asyncio.sleep(2)
        # await page.locator('input[type=file][accept^="image/"]').set_input_files(self.cover_path)
        # # 点击确认
        # await asyncio.sleep(3)
        # # await page.locator(f'xpath=/html/body/div[1]/div[1]/div[1]/main/div/div/div[1]/div/div/haploid-html/haploid-body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/button[1]/span').click()
        # await page.locator('button.ant-btn.ant-btn-primary:has-text("确认")').first.click()
        # await asyncio.sleep(5)


        # 新版
        # 悬浮 _default-cover_y5cqm_68 _big_y5cqm_77
        await page.locator('._default-cover_y5cqm_68._big_y5cqm_77').hover()
        await page.locator('._cover-editor-text_y5cqm_58:has-text("编辑")').click()
        await page.locator('.ant-btn.ant-btn-default:has-text("重选封面")').click()
        await page.locator('#microSupport input[type=file][accept^="image/"]').set_input_files(self.cover_path)
        await page.locator('.ant-btn.ant-btn-default._footer-btn_1nlbi_40:has-text("完成")').click()


        # await asyncio.sleep(10000)
        # 点击发布按钮
        # await page.locator('button:has-text("发布")').click()
        await page.locator('._button_si04s_1._button-primary_si04s_60:has-text("发布")').click()


        # if self.publish_date != 0:
        #     # 快手最后还要点击一次确认发布
        #     asyncio.sleep(0.5)
        #     # await page.locator('button.ant-btn.ant-btn-primary:has-text("确认发布")').click()
        #     await page.locator('button:has-text("确认发布")').click()

        await context.storage_state(path=self.account_file)  # 保存cookie
        print('  [-]cookie更新完毕！')

        await asyncio.sleep(1)
       
        # 关闭浏览器上下文和浏览器实例
        await context.close()
        await browser.close()
        
    
    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)



if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    fullpath = config['path']+config['dir']
    print(fullpath)
    # videoFile = getFileNames(fullpath)
    # print(f"{fullpath} 文件夹下有 {len(videoFile)} 个视频")
    
    account_file = 'kuaishou.json'
    
    # publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    # cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
    
    tags=["我的世界","mc不灭",'撒旦发射点']
    file= r"D:\desktop\myself\video\我的世界：变成钻石骷髅在MC中生存100天！【第1集】.mp4"
    title="我的世界：变成在MC中生存100天【第一集】"
    cover=r"D:\desktop\myself\videos\image1.png"
    app = KuaiShouVideo(title, file, cover, tags, datetime(2024, 3, 25, 10, 30, 0), account_file)
    asyncio.run(app.main(), debug=False)