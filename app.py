import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import zlib
import platform

# --- CONFIGURATION ---
st.set_page_config(page_title="OBSCURA 2025", page_icon="👁️", layout="centered")

# --- CSS (THE ORACLE AESTHETIC) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Cinzel', serif;
        text-align: center;
        letter-spacing: 5px;
        color: #f0f0f0;
        font-size: 2.5rem !important;
        text-transform: uppercase;
    }
    
    .stFileUploader {
        border: 1px solid #333;
        padding: 40px;
        background-color: #0a0a0a;
    }
    
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border: none;
        width: 100%;
        padding: 20px;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #a8dadc; /* Pale Cyan */
        box-shadow: 0px 0px 20px rgba(168, 218, 220, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- THE ARCHETYPE DATABASE (20 DISTINCT IDENTITIES) ---
ARCHETYPES = [
    {"NAME": "THE NIGHTCRAWLER", "ANIMAL": "RACCOON", "DISH": "MIDNIGHT MAGGI", "FILM": "FIGHT CLUB", "APP": "DISCORD", "CITY": "BERLIN", "HOBBY": "DOOMSCROLLING", "COLOR": (142, 68, 173)},
    {"NAME": "THE VISIONARY", "ANIMAL": "FALCON", "DISH": "DOUBLE ESPRESSO", "FILM": "INTERSTELLAR", "APP": "NOTION", "CITY": "SILICON VALLEY", "HOBBY": "BUILDING EMPIRES", "COLOR": (41, 128, 185)},
    {"NAME": "THE MAINSTREAM", "ANIMAL": "GOLDEN RETRIEVER", "DISH": "DOMINOS PIZZA", "FILM": "YEH JAWAANI HAI DEEWANI", "APP": "INSTAGRAM", "CITY": "MUMBAI", "HOBBY": "CAFE HOPPING", "COLOR": (230, 126, 34)},
    {"NAME": "THE MYSTIC", "ANIMAL": "OWL", "DISH": "CHAMOMILE TEA", "FILM": "EAT PRAY LOVE", "APP": "HEADSPACE", "CITY": "VARANASI", "HOBBY": "STARGAZING", "COLOR": (26, 188, 156)},
    {"NAME": "THE REBEL", "ANIMAL": "BLACK PANTHER", "DISH": "SPICY RAMEN", "FILM": "JOKER", "APP": "TELEGRAM", "CITY": "TOKYO", "HOBBY": "BREAKING RULES", "COLOR": (192, 57, 43)},
    {"NAME": "THE AESTHETIC", "ANIMAL": "SWAN", "DISH": "AVOCADO TOAST", "FILM": "LA LA LAND", "APP": "PINTEREST", "CITY": "PARIS", "HOBBY": "CURATING VIBES", "COLOR": (255, 105, 180)},
    {"NAME": "THE HUSTLER", "ANIMAL": "SHARK", "DISH": "PROTEIN SHAKE", "FILM": "WOLF OF WALL STREET", "APP": "LINKEDIN", "CITY": "NEW YORK", "HOBBY": "DAY TRADING", "COLOR": (39, 174, 96)},
    {"NAME": "THE NOMAD", "ANIMAL": "TURTLE", "DISH": "DAL CHAWAL", "FILM": "INTO THE WILD", "APP": "GOOGLE MAPS", "CITY": "MANALI", "HOBBY": "GETTING LOST", "COLOR": (241, 196, 15)},
    {"NAME": "THE GLITCH", "ANIMAL": "CHAMELEON", "DISH": "ENERGY DRINK", "FILM": "THE MATRIX", "APP": "REDDIT", "CITY": "SEOUL", "HOBBY": "GAMING", "COLOR": (0, 255, 0)},
    {"NAME": "THE OLD SOUL", "ANIMAL": "ELEPHANT", "DISH": "GHAR KA KHANA", "FILM": "THE GODFATHER", "APP": "WHATSAPP", "CITY": "KOLKATA", "HOBBY": "READING HISTORY", "COLOR": (121, 85, 72)},
    {"NAME": "THE CREATOR", "ANIMAL": "OCTOPUS", "DISH": "SUSHI PLATTER", "FILM": "INCEPTION", "APP": "FIGMA", "CITY": "LONDON", "HOBBY": "DESIGNING", "COLOR": (155, 89, 182)},
    {"NAME": "THE MINIMALIST", "ANIMAL": "CAT", "DISH": "SALAD", "FILM": "HER", "APP": "NOTES", "CITY": "COPENHAGEN", "HOBBY": "DECLUTTERING", "COLOR": (189, 195, 199)},
    {"NAME": "THE CHAOS", "ANIMAL": "MONKEY", "DISH": "VADA PAV", "FILM": "HERA PHERI", "APP": "TWITTER (X)", "CITY": "DELHI", "HOBBY": "STARTING DRAMA", "COLOR": (255, 0, 0)},
    {"NAME": "THE SCHOLAR", "ANIMAL": "RAVEN", "DISH": "DARK CHOCOLATE", "FILM": "DEAD POETS SOCIETY", "APP": "GOODREADS", "CITY": "OXFORD", "HOBBY": "JOURNALING", "COLOR": (52, 73, 94)},
    {"NAME": "THE ROMANTIC", "ANIMAL": "DOVE", "DISH": "RED WINE", "FILM": "DILWALE DULHANIA...", "APP": "SPOTIFY", "CITY": "UDAIPUR", "HOBBY": "DAYDREAMING", "COLOR": (233, 30, 99)},
    {"NAME": "THE GYM RAT", "ANIMAL": "GORILLA", "DISH": "CHICKEN BREAST", "FILM": "ROCKY", "APP": "STRAVA", "CITY": "LOS ANGELES", "HOBBY": "LIFTING HEAVY", "COLOR": (44, 62, 80)},
    {"NAME": "THE TECHIE", "ANIMAL": "ROBOT", "DISH": "PIZZA POCKETS", "FILM": "SOCIAL NETWORK", "APP": "GITHUB", "CITY": "BANGALORE", "HOBBY": "CODING", "COLOR": (0, 150, 255)},
    {"NAME": "THE PARTY", "ANIMAL": "PEACOCK", "DISH": "SHOTS", "FILM": "THE HANGOVER", "APP": "SNAPCHAT", "CITY": "GOA", "HOBBY": "AFTER PARTIES", "COLOR": (255, 20, 147)},
    {"NAME": "THE HEALER", "ANIMAL": "DEER", "DISH": "SMOOTHIE BOWL", "FILM": "SOUL", "APP": "CALM", "CITY": "RISHIKESH", "HOBBY": "YOGA", "COLOR": (100, 255, 100)},
    {"NAME": "THE ENIGMA", "ANIMAL": "WOLF", "DISH": "BLACK WATER", "FILM": "DONNIE DARKO", "APP": "SIGNAL", "CITY": "REYKJAVIK", "HOBBY": "DISAPPEARING", "COLOR": (80, 80, 80)}
]

# --- THE LOGIC ENGINE ---

def get_deterministic_identity(img):
    """
    Calculates a numeric hash from the image bytes.
    This ensures the SAME photo always yields the SAME result.
    """
    # 1. Resize for consistent processing
    small = img.resize((50, 50))
    # 2. Convert to bytes
    img_bytes = small.tobytes()
    # 3. Calculate Checksum (Hash)
    hash_val = zlib.adler32(img_bytes)
    
    # 4. Use Hash to pick Index
    index = hash_val % len(ARCHETYPES)
    return ARCHETYPES[index]

def load_fonts():
    """Smart font loader that works on both Windows and Cloud."""
    system = platform.system()
    fonts = {}
    
    try:
        if system == "Windows":
            # Use Standard Windows Fonts
            fonts['hero'] = ImageFont.truetype("arialbd.ttf", 90)
            fonts['title'] = ImageFont.truetype("arialbd.ttf", 40)
            fonts['label'] = ImageFont.truetype("calibri.ttf", 30)
            fonts['val'] = ImageFont.truetype("timesbd.ttf", 50)
            fonts['credit'] = ImageFont.truetype("calibri.ttf", 24)
        else:
            # Use Standard Linux/Cloud Fonts
            fonts['hero'] = ImageFont.truetype("DejaVuSerif-Bold.ttf", 90)
            fonts['title'] = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            fonts['label'] = ImageFont.truetype("DejaVuSans.ttf", 28)
            fonts['val'] = ImageFont.truetype("DejaVuSerif-Bold.ttf", 50)
            fonts['credit'] = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        # Fallback to default if anything breaks
        default = ImageFont.load_default()
        fonts = {k: default for k in ['hero', 'title', 'label', 'val', 'credit']}
        
    return fonts

def create_card(uploaded_img):
    # CANVAS: 1080x1920 (Instagram Story)
    W, H = 1080, 1920
    bg_color = (10, 10, 12) 
    
    img = Image.new('RGB', (W, H), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Process Image
    raw = Image.open(uploaded_img).convert("RGB")
    
    # GET IDENTITY
    identity = get_deterministic_identity(raw)
    accent_color = identity["COLOR"]
    
    # LOAD FONTS
    fonts = load_fonts()

    # 1. IMAGE DISPLAY (Square + Border)
    target_s = 800
    raw = ImageOps.fit(raw, (target_s, target_s), centering=(0.5, 0.5))
    raw = ImageOps.expand(raw, border=5, fill=accent_color)
    
    # Center the image perfectly
    img_x = (W - (target_s + 10)) // 2
    img.paste(raw, (img_x, 220))
    
    # 2. HEADER
    d.text((W//2, 100), "THE OBSCURA", fill=(255, 255, 255), font=fonts['hero'], anchor="ms")
    d.text((W//2, 170), "2025 IDENTITY REVEAL", fill=(150, 150, 150), font=fonts['label'], anchor="ms")
    
    # 3. IDENTITY NAME (The Box)
    d.rectangle([100, 1080, 980, 1150], outline=accent_color, width=3)
    d.text((W//2, 1115), identity["NAME"], fill=accent_color, font=fonts['title'], anchor="mm")
    
    # 4. ATTRIBUTES GRID
    start_y = 1250
    items = [
        ("SPIRIT ANIMAL", identity["ANIMAL"]),
        ("SOUL DISH", identity["DISH"]),
        ("THE FILM", identity["FILM"]),
        ("THE APP", identity["APP"]),
        ("THE CITY", identity["CITY"]),
        ("THE HOBBY", identity["HOBBY"])
    ]
    
    # Loop for items
    for label, value in items:
        # Label (Left)
        d.text((120, start_y), label, fill=(100, 100, 100), font=fonts['label'], anchor="ls")
        # Value (Right)
        d.text((960, start_y), value, fill=(255, 255, 255), font=fonts['val'], anchor="rs")
        # Line
        d.line([(120, start_y + 10), (960, start_y + 10)], fill=(30, 30, 30), width=1)
        start_y += 90 # Adjusted gap to fit better
        
    # 5. FOOTER (MINIMALIST SIGNATURE)
    d.text((W//2, H - 80), "@THEOBSCURA_17", fill=accent_color, font=fonts['credit'], anchor="ms")
    
    # 6. FINAL TOUCH: OUTER GLOW BORDER
    d.rectangle([0, 0, W-1, H-1], outline=accent_color, width=5)
    
    return img

# --- UI ---
st.title("THE OBSCURA")
st.markdown("*Upload a photo. The Oracle will read your 2025 Energy.*")

uploaded_file = st.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

if st.button("REVEAL MY IDENTITY"):
    if not uploaded_file:
        st.error("UPLOAD REQUIRED FOR READING.")
    else:
        # No spinner for instant gratification
        card = create_card(uploaded_file)
        st.success("IDENTITY DECODED. THIS IS YOUR TRUTH FOR 2025.")
        st.image(card, caption="YOUR 2025 CARD", use_container_width=True)
        
        st.markdown("<p style='text-align: center; color: #888;'>Does this resonate? Share your card to find your tribe.</p>", unsafe_allow_html=True)
        
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.download_button("SAVE & CLAIM YOUR IDENTITY", buf.getvalue(), "OBSCURA_2025.png", "image/png")
