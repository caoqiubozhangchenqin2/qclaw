from PIL import Image, ImageDraw, ImageFont
import os

# --- 画布设置 ---
W, H = 1080, 1920
img = Image.new("RGB", (W, H), "#1a1a2e")
draw = ImageDraw.Draw(img)

# --- 字体 ---
font_bold = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 56)
font_sub = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 40)
font_body = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 34)
font_body_sm = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
font_price = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 48)
font_price_sm = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
font_tag = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 26)
font_qr = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 30)

# --- 颜色 ---
GOLD = "#f0c040"
ORANGE = "#ff6b35"
WHITE = "#ffffff"
LIGHT = "#e0e0e0"
DARK_BG = "#1a1a2e"
CARD_BG = "#2a2a4a"
ACCENT = "#ff4757"

# --- 顶部装饰条 ---
for y in range(12):
    alpha = 255 - y * 20
    draw.rectangle([(0, y), (W, y+1)], fill=GOLD)

# --- 顶部标签 ---
tag_text = "2026 暑假班"
bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
draw.rounded_rectangle([(W//2 - tw//2 - 30, 40), (W//2 + tw//2 + 30, 40 + th + 20)], radius=30, fill=ORANGE)
draw.text((W//2 - tw//2, 45), tag_text, fill=WHITE, font=font_tag)

# --- 主标题 ---
y = 130
title1 = "音为热爱"
title2 = "乐动一夏"
draw.text((W//2 - draw.textbbox((0,0), title1, font=font_bold)[2]//2, y), title1, fill=GOLD, font=font_bold)
y += 100
draw.text((W//2 - draw.textbbox((0,0), title2, font=font_bold)[2]//2, y), title2, fill=WHITE, font=font_bold)

# --- 副标题 ---
y += 110
sub = "山前坊文创街区 · 小之之乐器"
draw.text((W//2 - draw.textbbox((0,0), sub, font=font_sub)[2]//2, y), sub, fill=LIGHT, font=font_sub)

# --- 分隔线 ---
y += 70
draw.rectangle([(100, y), (W-100, y+2)], fill=GOLD)

# --- 课程列表 ---
y += 30
courses = [
    ("🎸 民谣吉他", "零基础弹唱入门"),
    ("⚡ 电吉他", "摇滚启蒙/即兴solo"),
    ("🎹 钢  琴", "古典/流行双线教学"),
    ("🥁 架子鼓", "节奏感培养/律动训练"),
    ("🎵 尤克里里", "轻松上手/弹唱一体"),
    ("🏮 古  筝", "传统民乐/国风曲目"),
]
for name, desc in courses:
    draw.text((100, y), name, fill=WHITE, font=font_body)
    draw.text((420, y + 6), desc, fill=LIGHT, font=font_body_sm)
    y += 52

# --- 套餐卡片 ---
y += 30
draw.rectangle([(80, y), (W-80, y+2)], fill="#3a3a5a")
y += 20

packages = [
    ("🔥 启蒙班", "499元/8节", "零基础入门，1种乐器", ORANGE),
    ("⭐ 进阶班", "960元/12节", "1对1/2人小班，含汇报演出", GOLD),
    ("🎓 成人班", "999元/16节", "高中毕业生/成人专属，灵活约课", ACCENT),
]

for title, price, desc, color in packages:
    # 卡片背景
    draw.rounded_rectangle([(80, y), (W-80, y+130)], radius=16, fill=CARD_BG)
    # 左侧色条
    draw.rectangle([(80, y+10), (88, y+120)], fill=color)
    # 标题
    draw.text((110, y+12), title, fill=color, font=font_sub)
    # 价格
    draw.text((110, y+60), price, fill=WHITE, font=font_price)
    # 描述
    desc_x = 110 + draw.textbbox((0,0), price, font=font_price)[2] + 20
    draw.text((desc_x, y+72), desc, fill=LIGHT, font=font_price_sm)
    y += 150

# --- 亮点区 ---
y += 20
draw.rectangle([(80, y), (W-80, y+2)], fill="#3a3a5a")
y += 25

highlights = [
    "✅ YAMAHA吉他常熟地区授权代理商",
    "✅ 免费体验课｜逛街路过就进来试一把",
    "✅ 老带新各送1节｜口碑裂变",
    "✅ 汇报演出｜让孩子站上山前坊的舞台",
    "✅ 灵活排课｜暑假随时约课",
]
for h in highlights:
    draw.text((100, y), h, fill=LIGHT, font=font_body_sm)
    y += 48

# --- 底部信息区 ---
y += 30
draw.rectangle([(0, y), (W, H)], fill="#15152a")
y += 30
draw.text((100, y), "📍 常熟市山前坊文创街区（虞山脚下）", fill=LIGHT, font=font_body)
y += 50
draw.text((100, y), "🔥 高考结束即开课！名额有限，先到先得", fill=ORANGE, font=font_body)
y += 60

# 扫码提示
draw.text((100, y), "📲 扫码预约免费体验课", fill=WHITE, font=font_sub)

# QR占位框
qr_y = y + 60
draw.rounded_rectangle([(100, qr_y), (300, qr_y+200)], radius=12, fill=CARD_BG, outline=GOLD, width=2)
draw.text((140, qr_y+75), "[二维码]", fill=LIGHT, font=font_body)

# 联系方式
draw.text((340, qr_y+20), "📞 咨询电话", fill=GOLD, font=font_body)
draw.text((340, qr_y+65), "155-0613-1722", fill=WHITE, font=font_body)
draw.text((340, qr_y+120), "💬 微信同号", fill=LIGHT, font=font_body_sm)

# --- 底部品牌 ---
draw.text((W//2 - draw.textbbox((0,0), "小之之乐器", font=font_tag)[2]//2, H-60), "小之之乐器", fill="#5a5a7a", font=font_tag)

# --- 保存 ---
out_path = r"C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\暑期招生海报.png"
img.save(out_path, "PNG")
print(f"OK: {out_path}")
