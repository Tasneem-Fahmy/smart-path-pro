import streamlit as st
from datetime import datetime
import random
from streamlit_drawable_canvas import st_canvas

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="سمارت باث برو | Smart Path Pro", layout="wide")

# --- 2. قائمة الـ 50 رسالة (عتاب وتشجيع) ---
messages_50 = [
    "وقتك عدى، بس البطل الحقيقي بيقوم تاني ويكمل.", "الكسل عدو النجاح، يلا نعوض اللي فات!", "زعلتني منك، المهمة دي كانت مهمة، ابدأي دلوقتي.",
    "مفيش نجاح من غير التزام، قومي خلصيها.", "فات الميعاد، بس لسه في أمل ننجزها.", "كل تأخيرة وفيها خيرة لو بدأنا فوراً.",
    "الذكاء الاصطناعي مبيستناش، شدي حيلك!", "ليه التأخير؟ أنتِ أقوى من كده.", "عتاب خفيف: كان ممكن نخلصها في وقتها.",
    "تسنيم المبدعة مبتسيبش مهامها كده، صح؟", "الوقت كالسيف، خلينا نركز أكتر.", "بلاش تراكمي الشغل، ابدأي حالاً.",
    "فرصة ضاعت، بس الجاي أحسن بكتير.", "النجاح بيحب الملتزمين، يلا نرجع للطريق.", "مفيش وقت للندم، في وقت للشغل.",
    "عادي نقع، بس مش عادي نفضل مكاننا.", "المهمة بتناديكي، متتجاهليهاش.", "تأخير بسيط، نقدر نعوضه بتركيز مضاعف.",
    "بلاش كسل، مستقبلك في 2027 مستنيكي.", "خليكي دايماً قد التحدي، خلصيها.", "النوم مش هيفيد، الإنجاز هو اللي بيفرح.",
    "كل دقيقة بتعدي محسوبة عليكي.", "توقعي من نفسك الأفضل دايماً.", "عتاب: الديدلاين مش مجرد رقم، ده التزام.",
    "يلا، امسحي الإحباط واكتبي إنجاز جديد.", "التسويف بيسرق الأحلام، انتبهي.", "أنتِ أشطر من إنك تسيبي دي تفوتك.",
    "خليكي فخورة بنفسك وخلصي اللي وراكي.", "الرحلة طويلة ومحتاجة نفس، كملي.", "بلاش أعذار، النتيجة هي اللي بتتكلم.",
    "المهمة دي زعلانة إنها متخلصتش.", "تذكري هدفك الأول، وقومي اشتغلي.", "خسارة الوقت هي أكبر خسارة.",
    "تقدرين، بس محتاجة شوية إرادة.", "العتاب ده لأننا واثقين في قدراتك.", "متخليش حاجة توقفك، حطمي الكسل.",
    "لسه الفرصة في إيدك، استغليها.", "الإنجاز المتأخر أحسن من عدم الإنجاز.", "بطلي تأجيل، وابدأي التنفيذ.",
    "خليكي قوية، المهام دي بتبني مستقبلك.", "تسنيم، الكاتبة والمبرمجة مبتستسلمش.", "الوقت اللي راح مش هيرجع، استغلي الباقي.",
    "عتاب أخير: ركزي في جدولك أكتر.", "كلنا بنغلط، الشاطر اللي بيتعلم.", "يلا نعمل 'تم الإنجاز' ونفرح.",
    "الفرحة بالإنجاز أحلى من راحة الكسل.", "مستنيين إبداعك، متتأخريش علينا.", "المهام دي درجات سلم لنجاحك.",
    "أنا جمبك وبشجعك، متخذلنيش.", "بدل ما نزعل على اللي فات، نخلص اللي في إيدينا."
]

# --- 3. محرك التصميم ---
def apply_css(is_dark):
    bg = "#121212" if is_dark else "#FFFFFF"
    text = "#FFFFFF" if is_dark else "#000000"
    sidebar_bg = "#1E1E1E" if is_dark else "#F0F2F6"
    card_bg = "#2D2D2D" if is_dark else "#F9F9F9"
    
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg}; color: {text}; direction: rtl; text-align: right; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; }}
        h1, h2, h3, p, label, div {{ color: {text} !important; }}
        .header-title {{ font-size: 35px; font-weight: bold; color: #007BFF !important; border-bottom: 2px solid #007BFF; padding-bottom: 10px; margin-bottom: 20px; }}
        .task-box {{ background-color: {card_bg}; padding: 15px; border-radius: 10px; border-right: 5px solid #007BFF; margin-bottom: 15px; }}
        .msg-box {{ background-color: #FF4B4B22; border-right: 5px solid #FF4B4B; padding: 10px; border-radius: 5px; margin-top: 10px; font-weight: bold; }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. تهيئة قاعدة البيانات ---
if 'db' not in st.session_state:
    st.session_state.db = {'tasks': [], 'arts': [], 'writings': [], 'sports': []}

# --- 5. التطبيق ---
def main():
    apply_css(st.sidebar.toggle("الوضع الداكن", value=True))
    
    # اسم الموقع ثابت في كل الصفحات
    st.markdown('<div class="header-title">سمارت باث برو | Smart Path Pro</div>', unsafe_allow_html=True)
    
    nav = st.sidebar.radio("القائمة الرئيسية:", ["المهام الدراسية", "المرسم والمكتبة", "أكاديمية الرياضة"])
    
    # ------------------ 1. المهام ------------------
    if nav == "المهام الدراسية":
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.subheader("إضافة مهمة جديدة")
            folder = st.text_input("اسم المجلد (اختياري)")
            name = st.text_input("وصف المهمة")
            d_date = st.date_input("تاريخ التسليم")
            d_time = st.time_input("الوقت")
            
            if st.button("حفظ المهمة"):
                deadline = datetime.combine(d_date, d_time)
                if deadline <= datetime.now():
                    st.error("❌ لا يمكن تسجيل مهمة وقتها انتهى في الماضي!")
                elif not name:
                    st.error("❌ يجب كتابة اسم المهمة.")
                else:
                    st.session_state.db['tasks'].append({
                        "id": random.randint(1000, 9999), "folder": folder, "name": name, 
                        "deadline": deadline, "done": False, "msg": ""
                    })
                    st.success("تم الحفظ بنجاح!")
                    st.rerun()

        with col2:
            st.subheader("لوحة المهام")
            if not st.session_state.db['tasks']: st.write("لا توجد مهام حالياً.")
            
            for i, t in enumerate(st.session_state.db['tasks']):
                # حساب الوقت
                now = datetime.now()
                is_past = t['deadline'] <= now
                
                # إعطاء رسالة عتاب لو الوقت فات ومادستش إتمام
                if is_past and not t['done'] and not t['msg']:
                    t['msg'] = random.choice(messages_50)
                
                with st.container():
                    st.markdown(f"""<div class="task-box">
                        <b>المجلد:</b> {t['folder'] if t['folder'] else 'عام'} <br>
                        <b>المهمة:</b> {t['name']} <br>
                        <b>الموعد:</b> {t['deadline'].strftime('%Y-%m-%d %H:%M')}
                    </div>""", unsafe_allow_html=True)
                    
                    if t['msg'] and not t['done']:
                        st.markdown(f'<div class="msg-box">⚠️ {t["msg"]}</div>', unsafe_allow_html=True)
                    
                    if not t['done']:
                        if st.button(f"إتمام المهمة 🎉", key=f"done_{t['id']}"):
                            t['done'] = True
                            st.balloons()
                            st.rerun()
                    else:
                        st.success("✅ تمت بنجاح!")
                    
                    # تعديل وحذف
                    with st.expander("إدارة وتعديل المهمة"):
                        new_folder = st.text_input("تعديل المجلد", t['folder'], key=f"f_{t['id']}")
                        new_name = st.text_input("تعديل الاسم", t['name'], key=f"n_{t['id']}")
                        if st.button("حفظ التعديل", key=f"e_{t['id']}"):
                            t['folder'], t['name'] = new_folder, new_name
                            st.rerun()
                        if st.button("❌ حذف المهمة", key=f"del_{t['id']}"):
                            st.session_state.db['tasks'].pop(i)
                            st.rerun()

    # ------------------ 2. المرسم والمكتبة ------------------
    elif nav == "المرسم والمكتبة":
        tab1, tab2 = st.tabs(["🎨 المرسم", "✍️ المكتبة"])
        
        # المرسم
        with tab1:
            st.subheader("أدوات الرسم المتخصصة")
            art_type = st.selectbox("اختر الفن", ["ديجيتال آرت", "رسم زيتي", "فحم", "ألوان مائية"])
            
            # تخصيص الأدوات حسب الفن
            if art_type == "فحم":
                st.write("تم تجهيز فرشاة دقيقة وخلفية ورق.")
                stroke_color = st.color_picker("لون الفحم", "#333333")
                bg_color = "#F4F1EA"
            elif art_type == "رسم زيتي":
                st.write("تم تجهيز فرشاة سميكة للدمج.")
                stroke_color = st.color_picker("اختر اللون الأساسي", "#8B4513")
                bg_color = "#FFFFFF"
            else:
                stroke_color = st.color_picker("اختر اللون", "#000000")
                bg_color = st.color_picker("لون الخلفية", "#FFFFFF")
            
            st_canvas(stroke_width=10, stroke_color=stroke_color, background_color=bg_color, height=300, key="art_canvas")
            
            art_status = st.radio("حالة اللوحة", ["تم الانتهاء", "الانتهاء لاحقاً"], key="art_stat")
            if art_status == "الانتهاء لاحقاً":
                art_dl = st.date_input("حدد موعد العودة للوحة")
            if st.button("حفظ اللوحة"): st.success("تم أرشفة اللوحة.")

        # المكتبة
        with tab2:
            st.subheader("أدوات الكتابة الاحترافية")
            write_type = st.selectbox("نوع الكتابة", ["رواية", "شعر", "سيناريو"])
            
            title = st.text_input("عنوان العمل")
            if write_type == "رواية":
                st.text_area("بناء العالم والشخصيات")
                content = st.text_area("أحداث الفصل")
            elif write_type == "شعر":
                st.text_input("الوزن والقافية المستهدفة")
                content = st.text_area("أبيات القصيدة")
            else:
                st.text_area("وصف المشهد (الزمان والمكان)")
                content = st.text_area("الحوار")
                
            w_status = st.radio("حالة النص", ["تم الإنجاز", "إكمال لاحقاً"], key="w_stat")
            if w_status == "إكمال لاحقاً":
                st.date_input("موعد إكمال النص")
            if st.button("حفظ الكتابة"): st.success("تم الحفظ في المكتبة.")

    # ------------------ 3. أكاديمية الرياضة ------------------
    elif nav == "أكاديمية الرياضة":
        st.subheader("أكاديمية تدريب المحترفين")
        sport = st.selectbox("اختر الرياضة", ["جيم", "كرة قدم", "سباحة", "إسكواش", "تنس", "سلة", "باليه", "كاراتيه", "كونغ فو"])
        
        # تفاصيل مخصصة جداً لكل رياضة
        if sport == "جيم":
            st.info("نصيحة الكابتن: حافظ على التنفس السليم وقت رفع الوزن، ومتنساش الإحماء.")
            sets = st.number_input("عدد المجاميع", min_value=1)
            reps = st.number_input("عدد العدات في المجموعة", min_value=1)
            calories = sets * reps * 2
        
        elif sport == "سباحة":
            st.info("نصيحة الكابتن: شد بطنك أثناء العوم عشان جسمك يفضل مفرود على المية ويقلل المقاومة.")
            style = st.selectbox("نوع العومة", ["حرة", "فراشة", "ظهر", "صدر"])
            laps = st.number_input("عدد اللفات (طول المسبح)", min_value=1)
            calories = laps * 15
            
        elif sport == "كرة قدم":
            st.info("نصيحة الكابتن: العب السهل والممتنع، اللمسة الأولى بتحدد مسار الهجمة كلها.")
            st.text_input("المركز الذي تم اللعب فيه")
            duration = st.number_input("مدة اللعب (دقائق)", min_value=1)
            calories = duration * 10
            
        elif sport == "إسكواش":
            st.info("نصيحة الكابتن: سيطر على الـ (T) في نص الملعب عشان تتحكم في رتم المباراة.")
            duration = st.number_input("مدة اللعب (دقائق)", min_value=1)
            calories = duration * 13
            
        elif sport == "باليه":
            st.info("نصيحة الكابتن: التركيز البصري في نقطة ثابتة بيحافظ على توازنك أثناء الدوران.")
            st.number_input("مدة تمارين المرونة (دقائق)", min_value=1)
            calories = 300
            
        elif sport in ["كاراتيه", "كونغ فو"]:
            st.info("نصيحة الكابتن: قوة الضربة بتيجي من دوران الوسط مش من الإيد بس.")
            st.text_input("اسم الكاتا أو التكنيك المتدرب عليه")
            calories = 400
            
        else:
            st.info(f"نصيحة الكابتن: استمتع بوقتك في الـ {sport} وركز على التوافق العضلي العصبي.")
            duration = st.number_input("المدة (دقائق)", min_value=1)
            calories = duration * 8

        st.success(f"🔥 معدل الحرق التقريبي: {calories} سُعر حراري")
        st.text_input("الفورمة أو الإنجاز المستهدف في هذه اللعبة (الهدف)")
        if st.button("تسجيل النشاط الرياضي"):
            st.success("عاش يا بطلة! تم تسجيل إنجازك الرياضي.")

if __name__ == "__main__":
    main()