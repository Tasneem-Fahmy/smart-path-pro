import streamlit as st
import random
from datetime import datetime, timedelta
import re
import json
import requests

st.set_page_config(page_title="Smart Path Pro", layout="wide", page_icon="🚀")

FIREBASE_URL = "https://smart-path-pro-default-rtdb.firebaseio.com"
FIREBASE_SECRET = "AhELNPSgMW3DrL3s9C8TusSplnWPjzsIoWxuXr2s"

def fb_get(path):
    try:
        r = requests.get(f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_SECRET}", timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def fb_set(path, data):
    try:
        requests.put(f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_SECRET}",
                     data=json.dumps(data), timeout=5)
    except:
        pass

def fb_push(path, data):
    try:
        r = requests.post(f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_SECRET}",
                          data=json.dumps(data), timeout=5)
        return r.json().get("name") if r.status_code == 200 else None
    except:
        return None

def fb_delete(path):
    try:
        requests.delete(f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_SECRET}", timeout=5)
    except:
        pass

MESSAGES_50 = [
    "وقتك عدى، بس البطل الحقيقي بيقوم تاني ويكمل! 💪",
    "الكسل عدو النجاح، يلا نعوض اللي فات! 🔥",
    "مفيش نجاح من غير التزام، قومي خلصيها! ⚡",
    "فات الميعاد، بس لسه في أمل ننجزها! 🌟",
    "كل تأخيرة وفيها خيرة لو بدأنا فوراً! ✨",
    "الذكاء الاصطناعي مبيستناش، شدي حيلك! 🤖",
    "ليه التأخير؟ أنتِ أقوى من كده! 🦁",
    "عتاب خفيف: كان ممكن نخلصها في وقتها 😅",
    "الوقت كالسيف، خلينا نركز أكتر! ⚔️",
    "بلاش تراكمي الشغل، ابدأي حالاً! 🚀",
    "فرصة ضاعت، بس الجاي أحسن بكتير! 🌅",
    "النجاح بيحب الملتزمين، يلا نرجع للطريق! 🏆",
    "مفيش وقت للندم، في وقت للشغل! ⏰",
    "عادي نقع، بس مش عادي نفضل مكاننا! 🌈",
    "المهمة بتناديكي، متتجاهليهاش! 📢",
    "تأخير بسيط، نقدر نعوضه بتركيز مضاعف! 🎯",
    "بلاش كسل، مستقبلك مستنيكي! 🌟",
    "خليكي دايماً قد التحدي! 💎",
    "النوم مش هيفيد، الإنجاز هو اللي بيفرح! ☀️",
    "كل دقيقة بتعدي محسوبة عليكي! ⏳",
    "توقعي من نفسك الأفضل دايماً! 🦋",
    "الديدلاين مش مجرد رقم، ده التزام! 📅",
    "يلا، امسحي الإحباط واكتبي إنجاز جديد! ✍️",
    "التسويف بيسرق الأحلام، انتبهي! ⚠️",
    "أنتِ أشطر من إنك تسيبي دي تفوتك! 🌺",
    "خليكي فخورة بنفسك وخلصي اللي وراكي! 🏅",
    "الرحلة طويلة ومحتاجة نفس، كملي! 🌊",
    "بلاش أعذار، النتيجة هي اللي بتتكلم! 🎤",
    "تذكري هدفك الأول، وقومي اشتغلي! 🎯",
    "خسارة الوقت هي أكبر خسارة! ⌛",
    "تقدرين، بس محتاجة شوية إرادة! 💪",
    "العتاب ده لأننا واثقين في قدراتك! 🤝",
    "متخليش حاجة توقفك، حطمي الكسل! 💥",
    "لسه الفرصة في إيدك، استغليها! 🌸",
    "الإنجاز المتأخر أحسن من عدم الإنجاز! ✅",
    "بطلي تأجيل، وابدأي التنفيذ! 🏃",
    "خليكي قوية، المهام دي بتبني مستقبلك! 🏗️",
    "الكاتبة والمبرمجة مبتستسلمش! 👩‍💻",
    "الوقت اللي راح مش هيرجع، استغلي الباقي! ⏰",
    "ركزي في جدولك أكتر! 📋",
    "كلنا بنغلط، الشاطر اللي بيتعلم! 📚",
    "يلا نعمل 'تم الإنجاز' ونفرح! 🎉",
    "الفرحة بالإنجاز أحلى من راحة الكسل! 🌈",
    "مستنيين إبداعك، متتأخريش علينا! 🎨",
    "المهام دي درجات سلم لنجاحك! 🪜",
    "أنا جمبك وبشجعك، متخذلنيش! 🤗",
    "بدل ما نزعل على اللي فات، نخلص اللي في إيدينا! 💫",
    "كل خطوة صغيرة بتقربك من حلمك الكبير! 🌠",
    "إنتِ مش بس بتخلصي مهمة، بتبني نفسك! 🏆",
    "الأبطال مبيتوقفوش، وإنتِ منهم! ⚡",
]

def apply_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif !important; }
    .stApp { background: #0D0D0D; color: #FFFFFF; direction: rtl; }
    [data-testid="stSidebar"] { background: #141414 !important; border-left: 1px solid #222; }
    .task-card {
        background: #1A1A2E;
        border: 1px solid #16213E;
        border-right: 4px solid #0F3460;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: all 0.3s;
    }
    .task-card:hover { border-right-color: #E94560; transform: translateX(-3px); }
    .task-card.overdue { border-right-color: #E94560; background: #1a0f0f; }
    .task-card.done { border-right-color: #00B894; background: #0f1a10; opacity: 0.7; }
    .msg-box {
        background: linear-gradient(135deg, #E9456022, #E9456044);
        border: 1px solid #E94560;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        font-weight: 700;
        color: #FF6B8A !important;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.8} }
    .home-icon {
        background: linear-gradient(135deg, #1A1A2E, #16213E);
        border: 2px solid #0F3460;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s;
        margin: 10px;
    }
    .home-icon:hover {
        border-color: #E94560;
        transform: translateY(-8px);
        box-shadow: 0 15px 35px #E9456033;
    }
    .home-icon .icon { font-size: 64px; }
    .home-icon .title { font-size: 22px; font-weight: 700; color: #E0E0E0; margin-top: 10px; }
    .home-icon .sub { font-size: 13px; color: #888; margin-top: 5px; }
    .main-title {
        font-size: 38px;
        font-weight: 900;
        background: linear-gradient(90deg, #0F3460, #E94560);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 10px 0 5px;
    }
    .notif-warn { background:#2d1f00; border:1px solid #FFA500; border-radius:8px; padding:8px 14px; color:#FFA500 !important; margin:5px 0; }
    .notif-danger { background:#2d0000; border:1px solid #E94560; border-radius:8px; padding:8px 14px; color:#E94560 !important; margin:5px 0; }
    .stButton > button {
        border-radius: 10px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover { transform: scale(1.03) !important; }
    .login-box {
        max-width: 420px;
        margin: 60px auto;
        background: #141414;
        border: 1px solid #222;
        border-radius: 20px;
        padding: 50px 40px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def email_to_key(email):
    return email.replace(".", "_").replace("@", "__at__")

def is_valid_gmail(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+\-]+@gmail\.com$', email.strip()))

def get_notifications(deadline: datetime):
    now = datetime.now()
    diff = deadline - now
    total_hours = diff.total_seconds() / 3600
    notifs = []
    if total_hours < 0:
        return []
    if total_hours <= 0.5:
        notifs.append(("🚨 تحذير أخير!", f"متبقي أقل من 30 دقيقة!", "danger"))
    elif total_hours <= 2:
        notifs.append(("⚠️ آخر إنباه", f"متبقي {round(total_hours, 1)} ساعة فقط!", "danger"))
    elif total_hours <= 6:
        notifs.append(("🔔 تذكير عاجل", f"متبقي {round(total_hours, 1)} ساعة", "warn"))
    elif total_hours <= 24:
        notifs.append(("📌 تذكير", f"متبقي أقل من يوم ({round(total_hours)}س)", "warn"))
    elif total_hours <= 72:
        notifs.append(("📅 تذكير", f"متبقي {int(total_hours//24)} يوم", "warn"))
    return notifs

def smart_notif_schedule(deadline: datetime, created_at: datetime):
    now = datetime.now()
    total_duration = (deadline - created_at).total_seconds() / 3600
    remaining = (deadline - now).total_seconds() / 3600
    if remaining < 0:
        return []
    notifs = []
    if remaining <= 0.5:
        notifs.append(("🚨", "تحذير أخير! متبقي أقل من 30 دقيقة!", "danger"))
        return notifs
    if remaining <= 2:
        notifs.append(("⚠️", f"اوشكت على الانتهاء! متبقي {round(remaining*60)} دقيقة", "danger"))
        return notifs
    if total_duration >= 168:
        if remaining <= 72:
            notifs.append(("🔔", f"متبقي 3 أيام على الموعد!", "warn"))
        elif remaining <= 24 * 3.5:
            pass
    elif total_duration >= 72:
        if remaining <= 24:
            notifs.append(("🔔", f"متبقي يوم واحد فقط!", "warn"))
    elif total_duration >= 24:
        if remaining <= 6:
            notifs.append(("🔔", f"متبقي {round(remaining)} ساعة!", "warn"))
    else:
        if remaining <= 2:
            notifs.append(("⚠️", f"متبقي {round(remaining*60)} دقيقة!", "danger"))
    return notifs

def page_login():
    st.markdown('<div class="main-title">🚀 Smart Path Pro</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;margin-bottom:30px'>منصتك الذكية للإنجاز والإبداع</p>", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("---")
        email = st.text_input("📧 أدخلي بريدك الإلكتروني (Gmail فقط)", placeholder="example@gmail.com")
        if st.button("دخول 🚀", use_container_width=True, type="primary"):
            email = email.strip().lower()
            if not is_valid_gmail(email):
                st.error("❌ يجب إدخال بريد Gmail صحيح (ينتهي بـ @gmail.com)")
            else:
                key = email_to_key(email)
                user_data = fb_get(f"users/{key}")
                if not user_data:
                    user_data = {"email": email, "tasks": {}, "writings": {}, "sports": {}}
                    fb_set(f"users/{key}", user_data)
                st.session_state.user_email = email
                st.session_state.user_key = key
                st.session_state.page = "home"
                st.rerun()

def page_home():
    st.markdown(f'<div class="main-title">🚀 Smart Path Pro</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#888'>أهلاً {st.session_state.user_email} 👋</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="home-icon">
            <div class="icon">📚</div>
            <div class="title">المهام الدراسية</div>
            <div class="sub">نظم وتابع مهامك بذكاء</div>
        </div>""", unsafe_allow_html=True)
        if st.button("افتح المهام", key="btn_tasks", use_container_width=True):
            st.session_state.page = "tasks"
            st.rerun()
    with col2:
        st.markdown("""<div class="home-icon">
            <div class="icon">✍️</div>
            <div class="title">ستوديو الكتابة</div>
            <div class="sub">قصص، شعر، سيناريو وأكتر</div>
        </div>""", unsafe_allow_html=True)
        if st.button("افتح الكتابة", key="btn_write", use_container_width=True):
            st.session_state.page = "writing"
            st.rerun()
    with col3:
        st.markdown("""<div class="home-icon">
            <div class="icon">🏆</div>
            <div class="title">أكاديمية الرياضة</div>
            <div class="sub">تتبع تمارينك وإنجازاتك</div>
        </div>""", unsafe_allow_html=True)
        if st.button("افتح الرياضة", key="btn_sport", use_container_width=True):
            st.session_state.page = "sports"
            st.rerun()

def page_tasks():
    st.markdown('<div class="main-title">📚 المهام الدراسية</div>', unsafe_allow_html=True)
    key = st.session_state.user_key
    tasks_raw = fb_get(f"users/{key}/tasks") or {}
    tasks = {k: v for k, v in tasks_raw.items()} if isinstance(tasks_raw, dict) else {}
    tab_new, tab_past, tab_list = st.tabs(["➕ مهمة جديدة", "📖 تسجيل إنجاز قديم", "📋 لوحة المهام"])
    with tab_new:
        with st.form("new_task_form"):
            name = st.text_input("📝 وصف المهمة *")
            folder = st.text_input("📁 المجلد / المادة (اختياري)")
            col1, col2 = st.columns(2)
            with col1:
                d_date = st.date_input("📅 تاريخ التسليم")
            with col2:
                d_time = st.time_input("⏰ الوقت")
            submitted = st.form_submit_button("💾 حفظ المهمة", use_container_width=True, type="primary")
        if submitted:
            if not name:
                st.error("❌ يجب كتابة اسم المهمة")
            else:
                deadline = datetime.combine(d_date, d_time)
                now = datetime.now()
                min_deadline = now + timedelta(hours=6)
                if deadline < min_deadline:
                    st.error(f"❌ الموعد يجب أن يكون بعد {min_deadline.strftime('%Y-%m-%d %H:%M')} على الأقل (6 ساعات من الآن)")
                else:
                    task = {
                        "name": name, "folder": folder,
                        "deadline": deadline.isoformat(),
                        "created_at": now.isoformat(),
                        "done": False, "overdue_msg": "",
                        "type": "new"
                    }
                    fb_push(f"users/{key}/tasks", task)
                    st.success("✅ تم حفظ المهمة بنجاح!")
                    st.rerun()
    with tab_past:
        st.info("📖 سجّلي هنا أي إنجاز مضى وقته عشان يتحفظ في سجلك")
        with st.form("past_task_form"):
            p_name = st.text_input("📝 اسم الإنجاز")
            col1, col2 = st.columns(2)
            with col1:
                p_start = st.date_input("🗓️ تاريخ البداية")
            with col2:
                p_end = st.date_input("🗓️ تاريخ الانتهاء")
            p_notes = st.text_area("📄 ملاحظات (اختياري)")
            submitted_p = st.form_submit_button("💾 حفظ الإنجاز", use_container_width=True)
        if submitted_p:
            if not p_name:
                st.error("❌ اكتبي اسم الإنجاز")
            elif p_end < p_start:
                st.error("❌ تاريخ الانتهاء يجب أن يكون بعد البداية")
            else:
                task = {
                    "name": p_name, "folder": "إنجازات سابقة",
                    "deadline": datetime.combine(p_end, datetime.min.time()).isoformat(),
                    "created_at": datetime.combine(p_start, datetime.min.time()).isoformat(),
                    "done": True, "overdue_msg": "", "notes": p_notes,
                    "type": "past"
                }
                fb_push(f"users/{key}/tasks", task)
                st.success("🎉 تم تسجيل إنجازك!")
                st.rerun()
    with tab_list:
        if not tasks:
            st.markdown("<p style='text-align:center;color:#888;padding:40px'>لا توجد مهام بعد، أضيفي أول مهمة! 🌟</p>", unsafe_allow_html=True)
        else:
            filter_opt = st.radio("عرض:", ["الكل", "غير منجزة", "منجزة"], horizontal=True)
            for tid, t in tasks.items():
                if filter_opt == "غير منجزة" and t.get("done"):
                    continue
                if filter_opt == "منجزة" and not t.get("done"):
                    continue
                deadline = datetime.fromisoformat(t["deadline"])
                created_at = datetime.fromisoformat(t.get("created_at", datetime.now().isoformat()))
                now = datetime.now()
                is_past = deadline < now
                is_done = t.get("done", False)
                card_class = "done" if is_done else ("overdue" if is_past else "task-card")
                status_icon = "✅" if is_done else ("🔴" if is_past else "🟡")
                st.markdown(f"""<div class="task-card {card_class}">
                    <b>{status_icon} {t['name']}</b><br>
                    <small style="color:#888">
                        📁 {t.get('folder','عام')} &nbsp;|&nbsp; 
                        📅 {deadline.strftime('%Y-%m-%d %H:%M')}
                    </small>
                </div>""", unsafe_allow_html=True)
                if not is_done and not is_past:
                    notifs = smart_notif_schedule(deadline, created_at)
                    for icon, msg, level in notifs:
                        css_class = "notif-danger" if level == "danger" else "notif-warn"
                        st.markdown(f'<div class="{css_class}">{icon} {msg}</div>', unsafe_allow_html=True)
                if is_past and not is_done:
                    if not t.get("overdue_msg"):
                        t["overdue_msg"] = random.choice(MESSAGES_50)
                        fb_set(f"users/{key}/tasks/{tid}/overdue_msg", t["overdue_msg"])
                    st.markdown(f'<div class="msg-box">⚠️ {t["overdue_msg"]}</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    if not is_done:
                        if st.button("🎉 إتمام المهمة", key=f"done_{tid}"):
                            fb_set(f"users/{key}/tasks/{tid}/done", True)
                            st.balloons()
                            st.rerun()
                with c2:
                    with st.expander("✏️ تعديل"):
                        new_name = st.text_input("الاسم", t['name'], key=f"en_{tid}")
                        new_folder = st.text_input("المجلد", t.get('folder',''), key=f"ef_{tid}")
                        if st.button("حفظ", key=f"esave_{tid}"):
                            fb_set(f"users/{key}/tasks/{tid}/name", new_name)
                            fb_set(f"users/{key}/tasks/{tid}/folder", new_folder)
                            st.rerun()
                with c3:
                    if st.button("🗑️ حذف", key=f"del_{tid}"):
                        fb_delete(f"users/{key}/tasks/{tid}")
                        st.rerun()
                st.markdown("---")

def page_writing():
    st.markdown('<div class="main-title">✍️ ستوديو الكتابة</div>', unsafe_allow_html=True)
    write_types = {
        "📖 رواية / قصة": "story",
        "🎭 شعر / قصيدة": "poetry",
        "🎬 سيناريو": "scenario",
        "💡 حكمة / مقولة": "quote",
        "📰 مقال": "article",
    }
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 📂 نوع الكتابة")
        selected = st.radio("", list(write_types.keys()), label_visibility="collapsed")
        w_type = write_types[selected]
        st.markdown("---")
        st.markdown("### 💡 مساعدة AI")
        ai_prompt = st.text_area("اكتبي فكرتك وهيساعدك", placeholder="مثلاً: قصة عن فتاة تحب الفضاء...")
        if st.button("🤖 اقتراح AI", use_container_width=True):
            if ai_prompt:
                st.session_state.ai_suggestion = f"💭 بناءً على فكرتك عن '{ai_prompt}': جربي تبدأي بمشهد افتتاحي قوي يجذب القارئ، واستخدمي الحواس الخمس لتصوير البيئة."
            else:
                st.warning("اكتبي فكرتك أولاً")
    with col2:
        st.markdown(f"### {selected}")
        if w_type == "story":
            title = st.text_input("📌 عنوان القصة")
            col_a, col_b = st.columns(2)
            with col_a:
                genre = st.selectbox("النوع الأدبي", ["خيال علمي", "رومانسي", "تشويق", "مغامرة", "واقعي", "فانتازيا"])
            with col_b:
                pov = st.selectbox("وجهة السرد", ["ضمير المتكلم (أنا)", "ضمير الغائب (هو/هي)", "ضمير المخاطب (أنت)"])
            st.markdown("**👥 الشخصيات**")
            characters = st.text_area("اكتبي أسماء وصفات الشخصيات", placeholder="مثال: سارة - فتاة شجاعة تحب المغامرة\nكريم - صديقها الوفي")
            st.markdown("**🌍 بناء العالم**")
            world = st.text_area("وصف الزمان والمكان والجو العام", placeholder="مصر عام 2050، مدينة ذكية...")
            st.markdown("**📖 المقدمة**")
            intro = st.text_area("ابدأي القصة هنا...", height=120)
            st.markdown("**🌀 تخيّل الخاتمة**")
            ending_vision = st.text_area("كيف تتخيلين نهاية القصة؟", height=80)
            st.markdown("**📝 أحداث الفصل الحالي**")
            content = st.text_area("اكتبي الأحداث...", height=150)
        elif w_type == "poetry":
            title = st.text_input("📌 عنوان القصيدة")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                meter = st.selectbox("البحر الشعري", ["حر", "الطويل", "الكامل", "البسيط", "الوافر", "المتقارب", "الرمل", "الخفيف"])
            with col_b:
                rhyme = st.text_input("حرف القافية", placeholder="مثل: اء، ون")
            with col_c:
                mood = st.selectbox("المشاعر", ["حب", "حزن", "فرح", "حنين", "وطنية", "فلسفي"])
            st.markdown("**💡 نصائح البحر المختار:**")
            meter_tips = {
                "الطويل": "يُبنى على: فعولن مفاعيلن فعولن مفاعيلن",
                "الكامل": "يُبنى على: متفاعلن متفاعلن متفاعلن",
                "البسيط": "يُبنى على: مستفعلن فاعلن مستفعلن فاعلن",
                "حر": "لا قيود على الوزن، الإيقاع من الموسيقى الداخلية",
            }
            st.info(meter_tips.get(meter, "اختاري البحر المناسب لمشاعرك"))
            content = st.text_area("✍️ اكتبي أبياتك هنا...", height=250, placeholder="البيت الأول...\nالبيت الثاني...")
            characters = world = intro = ending_vision = ""
        elif w_type == "scenario":
            title = st.text_input("📌 عنوان العمل")
            col_a, col_b = st.columns(2)
            with col_a:
                scene_no = st.number_input("رقم المشهد", min_value=1, value=1)
            with col_b:
                scene_type = st.selectbox("نوع المشهد", ["داخلي", "خارجي", "فلاش باك"])
            st.markdown("**🎬 وصف المشهد**")
            world = st.text_area("الزمان / المكان / الإضاءة / الجو العام")
            st.markdown("**🎭 الشخصيات في المشهد**")
            characters = st.text_input("أسماء الشخصيات", placeholder="كريم، سارة، الأم")
            st.markdown("**💬 الحوار**")
            content = st.text_area("اكتبي الحوار بالشكل المسرحي:\nكريم: ...\nسارة: ...", height=200)
            intro = ending_vision = ""
        elif w_type == "quote":
            title = st.text_input("📌 موضوع الحكمة")
            content = st.text_area("✍️ اكتبي حكمتك أو مقولتك", height=150)
            st.markdown("**🔍 مرادفات وأفكار مساعدة:**")
            st.info("الحكمة الجيدة: قصيرة، معبّرة، تحمل فكرة كاملة في جملة واحدة")
            characters = world = intro = ending_vision = ""
        else:
            title = st.text_input("📌 عنوان المقال")
            col_a, col_b = st.columns(2)
            with col_a:
                article_type = st.selectbox("النوع", ["رأي", "تحليلي", "تعليمي", "إخباري"])
            with col_b:
                audience = st.selectbox("الجمهور المستهدف", ["عام", "متخصص", "شباب", "أطفال"])
            intro = st.text_area("📌 المقدمة", height=80)
            content = st.text_area("📄 جسم المقال", height=200)
            ending_vision = st.text_area("🔚 الخاتمة", height=80)
            characters = world = ""
        if hasattr(st.session_state, 'ai_suggestion'):
            st.success(st.session_state.ai_suggestion)
        st.markdown("---")
        col_s, col_b2 = st.columns([2, 1])
        with col_s:
            status = st.radio("حالة العمل:", ["✅ تم الإنجاز", "⏳ إكمال لاحقاً"], horizontal=True)
        with col_b2:
            if "لاحقاً" in status:
                remind_date = st.date_input("موعد الإكمال")
        if st.button("💾 حفظ العمل", use_container_width=True, type="primary"):
            wkey = st.session_state.user_key
            writing = {
                "title": title if 'title' in dir() else "",
                "type": w_type,
                "content": content if 'content' in dir() else "",
                "status": "done" if "تم" in status else "pending",
                "created_at": datetime.now().isoformat(),
            }
            fb_push(f"users/{wkey}/writings", writing)
            st.success("💾 تم الحفظ في مكتبتك!")

def page_sports():
    st.markdown('<div class="main-title">🏆 أكاديمية الرياضة</div>', unsafe_allow_html=True)
    sports_data = {
        "🏋️ جيم": {
            "tip": "حافظ على التنفس السليم وقت رفع الوزن، ومتنساش الإحماء.",
            "fields": ["sets", "reps", "weight"],
            "cal_formula": lambda d: d.get("sets", 0) * d.get("reps", 0) * d.get("weight", 0) * 0.1
        },
        "🏊 سباحة": {
            "tip": "شد بطنك أثناء العوم عشان جسمك يفضل مفرود على الماء.",
            "fields": ["laps", "style"],
            "cal_formula": lambda d: d.get("laps", 0) * 15
        },
        "⚽ كرة قدم": {
            "tip": "اللمسة الأولى بتحدد مسار الهجمة كلها.",
            "fields": ["duration", "position"],
            "cal_formula": lambda d: d.get("duration", 0) * 10
        },
        "🎾 إسكواش": {
            "tip": "سيطر على الـ T في منتصف الملعب عشان تتحكم في رتم المباراة.",
            "fields": ["duration"],
            "cal_formula": lambda d: d.get("duration", 0) * 13
        },
        "🎾 تنس": {
            "tip": "الضربة الأساسية هي الـ forehand، اتقنيها أولاً.",
            "fields": ["duration", "sets_won"],
            "cal_formula": lambda d: d.get("duration", 0) * 9
        },
        "🏀 كرة سلة": {
            "tip": "الدفاع بيكسب البطولات، ركز على الموقع الصحيح.",
            "fields": ["duration", "points"],
            "cal_formula": lambda d: d.get("duration", 0) * 8
        },
        "🩰 باليه": {
            "tip": "التركيز البصري في نقطة ثابتة بيحافظ على توازنك أثناء الدوران.",
            "fields": ["duration", "technique"],
            "cal_formula": lambda d: d.get("duration", 0) * 6
        },
        "🥋 كاراتيه / كونغ فو": {
            "tip": "قوة الضربة بتيجي من دوران الوسط مش من الإيد بس.",
            "fields": ["duration", "kata"],
            "cal_formula": lambda d: d.get("duration", 0) * 11
        },
    }
    sport = st.selectbox("🏅 اختاري الرياضة", list(sports_data.keys()))
    info = sports_data[sport]
    st.info(f"💡 نصيحة الكابتن: {info['tip']}")
    data = {}
    col1, col2 = st.columns(2)
    if "sets" in info["fields"]:
        with col1:
            data["sets"] = st.number_input("عدد المجاميع", min_value=0, value=3)
        with col2:
            data["reps"] = st.number_input("عدد العدات", min_value=0, value=10)
        data["weight"] = st.number_input("الوزن (كجم)", min_value=0, value=20)
    if "laps" in info["fields"]:
        with col1:
            data["laps"] = st.number_input("عدد اللفات", min_value=0, value=10)
        with col2:
            data["style"] = st.selectbox("نوع العومة", ["حرة", "فراشة", "ظهر", "صدر"])
    if "duration" in info["fields"]:
        with col1:
            data["duration"] = st.number_input("المدة (دقائق)", min_value=0, value=45)
    if "position" in info["fields"]:
        with col2:
            data["position"] = st.text_input("المركز", placeholder="مهاجم، وسط...")
    if "points" in info["fields"]:
        with col2:
            data["points"] = st.number_input("النقاط المسجلة", min_value=0)
    if "sets_won" in info["fields"]:
        with col2:
            data["sets_won"] = st.number_input("الأشواط المكسوبة", min_value=0)
    if "kata" in info["fields"]:
        data["kata"] = st.text_input("اسم الكاتا أو التكنيك")
    if "technique" in info["fields"]:
        data["technique"] = st.text_input("التقنية المتدربة عليها")
    target = st.text_input("🎯 الهدف من التمرين اليوم")
    try:
        calories = int(info["cal_formula"](data))
    except:
        calories = 0
    if calories > 0:
        st.success(f"🔥 معدل الحرق التقريبي: **{calories}** سعر حراري")
    if st.button("✅ تسجيل النشاط", use_container_width=True, type="primary"):
        skey = st.session_state.user_key
        activity = {
            "sport": sport, "data": data, "target": target,
            "calories": calories, "date": datetime.now().isoformat()
        }
        fb_push(f"users/{skey}/sports", activity)
        st.success("🎉 عاش يا بطلة! تم تسجيل إنجازك الرياضي!")
        st.balloons()
    with st.expander("📊 سجل أنشطتي"):
        skey = st.session_state.user_key
        sports_log = fb_get(f"users/{skey}/sports") or {}
        if sports_log:
            for sid, act in list(sports_log.items())[-10:]:
                date_str = datetime.fromisoformat(act["date"]).strftime("%Y-%m-%d") if "date" in act else "—"
                st.markdown(f"**{act['sport']}** — {date_str} — 🔥 {act.get('calories',0)} سعر")
        else:
            st.write("لا توجد أنشطة مسجلة بعد.")

def sidebar():
    with st.sidebar:
        st.markdown(f"**👤 المستخدم:**")
        st.markdown(f"<small style='color:#0F3460'>{st.session_state.get('user_email','')}</small>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**القائمة:**")
        pages = {"🏠 الرئيسية": "home", "📚 المهام": "tasks", "✍️ الكتابة": "writing", "🏆 الرياضة": "sports"}
        for label, pg in pages.items():
            active = "🔴" if st.session_state.get("page") == pg else "⚪"
            if st.button(f"{active} {label}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()
        st.markdown("---")
        if st.button("🚪 خروج", use_container_width=True):
            for k in ["user_email", "user_key", "page"]:
                st.session_state.pop(k, None)
            st.rerun()

def main():
    apply_css()
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if st.session_state.page == "login":
        page_login()
        return
    sidebar()
    page = st.session_state.get("page", "home")
    if page == "home":
        page_home()
    elif page == "tasks":
        page_tasks()
    elif page == "writing":
        page_writing()
    elif page == "sports":
        page_sports()

if __name__ == "__main__":
    main()
