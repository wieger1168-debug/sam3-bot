import streamlit as st
import os

# ============ КАРТА ПАМЯТИ СЭМА 3 (СТРУКТУРА АНКЕТЫ 2026) ============
# Связывает номера вопросов с понятными названиями для анализа
QUESTION_MAP = {
    # Раздел 1: Социально-демографический профиль
    "Q1": "Пол",
    "Q2": "Возраст",
    "Q3": "Место рождения",
    "Q4": "Где живёте",
    "Q5": "Семейное положение",
    "Q6": "Количество детей",
    "Q7": "Образование",
    "Q8": "Национальность",
    "Q9": "Язык обучения",
    "Q10": "Социальная группа",
    "Q11": "Статус",
    "Q12": "Личный доход",
    "Q13": "Семейный доход",
    "Q14": "Благосостояние",
    # Раздел 2: Религиозность и ценности
    "Q15": "Текущая религия",
    "Q16": "Предыдущая религия",
    "Q17": "Год принятия религии",
    "Q18_1": "Идентичность 1-я",
    "Q18_2": "Идентичность 2-я",
    "Q18_3": "Идентичность 3-я",
    "Q18_4": "Идентичность 4-я",
    "Q18_5": "Идентичность 5-я",
    "Q19": "Место России в мире",
    "Q20": "Переориентация на Восток",
    "Q21": "Окружающая действительность",
    "Q22": "Процессы в России и мире",
    "Q23_1": "Электронные ресурсы: досуг",
    "Q23_2": "Электронные ресурсы: наука",
    "Q23_3": "Электронные ресурсы: альтернативные движения",
    "Q23_4": "Электронные ресурсы: религиозные",
    "Q24": "Чтение священных книг",
    "Q25": "Чтение религиозной литературы",
    "Q26": "Отношение к успеху",
    "Q27": "Литература о НРД",
    "Q28": "Мировое правительство / антихрист",
    "Q29": "Развитие IT-технологий",
    "Q30": "Определение брака",
    "Q31": "Отношение к деторождению",
    "Q32": "Отношение к абортам",
    # Раздел 3: Геополитика и межконфессиональные отношения
    "Q33_1": "Будущее РФ: СССР",
    "Q33_2": "Будущее РФ: Многополярность",
    "Q33_3": "Будущее РФ: Империя",
    "Q33_4": "Будущее РФ: Глобальный Запад",
    "Q33_5": "Будущее РФ: Восток",
    "Q34": "Отношение к Православию",
    "Q35": "Отношение к Исламу",
    "Q36": "Сотрудничество РО с государством",
    # Раздел 4: Религиозная практика
    "Q37": "Частота посещения храма",
    "Q38": "Регулярность молитвы",
    "Q39": "Определение семьи",
    "Q40": "Тенденции развития человечества",
    "Q41": "Знание ФЗ о свободе совести",
    "Q42": "Соблюдение поста",
    "Q43": "Контроль гос-ва над РО",
    "Q44": "Отношение к Иудаизму",
    "Q45": "Отношение к НРД/оккультизму",
}

FILTER_KEYS = ["Q1", "Q2", "Q8", "Q15", "Q16", "Q34", "Q35", "Q44", "Q45"]

# ============ НАСТРОЙКИ СТРАНИЦЫ ============
st.set_page_config(
    page_title="СЭМ 3 — Вездеход по киберпространству",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ СТИЛИ: ПРИБОРНАЯ ДОСКА СЭМА ============
st.markdown("""
<style>
    .stApp { background-color: #0b0f0b; color: #d8e6d8; }

    .windshield {
        background: linear-gradient(180deg, #1a3a1a 0%, #2e5a2e 40%, #4a7a3a 70%, #6b8f4a 100%);
        border: 3px solid #66ff66;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        box-shadow: 0 0 25px rgba(102,255,102,0.35), inset 0 0 30px rgba(0,0,0,0.4);
        margin-bottom: 18px;
    }
    .windshield h1 {
        color: #eaffea; margin: 0;
        text-shadow: 2px 2px 6px #000;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
    }
    .windshield p { color: #cfe8cf; margin: 6px 0 0 0; font-style: italic; }

    .panel {
        background: #111711;
        border: 2px solid #3a5a3a;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: inset 0 0 12px rgba(0,0,0,0.6);
    }
    .panel h3 {
        color: #66ff66; font-family: 'Courier New', monospace;
        text-transform: uppercase; letter-spacing: 2px;
        border-bottom: 1px dashed #3a5a3a; padding-bottom: 6px;
    }

    .stTextInput input, .stSelectbox div, .stSlider div {
        background: #0e130e !important; color: #cfe8cf !important;
        border: 1px solid #3a5a3a !important;
    }
    .stCheckbox label { color: #d8e6d8 !important; }

    .stButton > button {
        background: linear-gradient(180deg, #2e7d32, #1b5e20);
        color: #eaffea; font-weight: bold;
        border: 2px solid #66ff66; border-radius: 8px;
        padding: 14px 30px; font-size: 18px;
        letter-spacing: 2px;
        box-shadow: 0 0 18px rgba(102,255,102,0.5);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #388e3c, #2e7d32);
        box-shadow: 0 0 30px rgba(102,255,102,0.8);
        transform: scale(1.02);
    }

    .route {
        background: #060a06; border: 2px solid #1f4d1f;
        border-radius: 8px; padding: 16px;
        font-family: 'Courier New', monospace; color: #5fff5f;
        box-shadow: inset 0 0 18px rgba(0,255,0,0.15);
    }
    .route h4 { color: #aaffaa; margin-top: 0; }

    .footer {
        text-align: center; color: #6b8f6b;
        font-family: 'Courier New', monospace;
        font-size: 13px; margin-top: 24px;
        border-top: 1px dashed #2e4a2e; padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============ ЛОГОТИП СЭМА (вид сбоку) ============
# Работает и локально, и в Streamlit Cloud (если файла нет — просто пропускаем)
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "sam_icon.png")
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True, caption="Сэм 3 · вид сбоку")
else:
    st.info("💡 Подсказка: положи файл sam_icon.png в папку с sam3.py — и Сэм появится в кабине!")

# ============ "ЛОБОВОЕ СТЕКЛО" — ШАПКА ============
st.markdown("""
<div class="windshield">
    <h1>🚙 СЭМ 3 · ВЕЗДЕХОД ПО КИБЕРПРОСТРАНСТВУ</h1>
    <p>«Ездит по сети так же уверенно, как Сэм 1 — по Ларамидии»</p>
</div>
""", unsafe_allow_html=True)

# ============ ПАНЕЛЬ 1: КУДА ЕДЕМ ============
st.markdown('<div class="panel"><h3>🎯 Навигатор · Куда едем?</h3></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    org = st.text_input("Конфессиональная организация", value="РОСХВЕ",
                        help="Например: РОСХВЕ, РЦХВЕ, ОЦХВЕ, РАНЦ ЕХБ, ХАСД РД")
with col2:
    region = st.text_input("Регион / территория",
                           value="Воркутинский городской округ, Республика Коми",
                           help="Город, район, область, край, республика")

# ============ ПАНЕЛЬ 2: РАЗДЕЛЫ МОНОГРАФИИ ============
st.markdown('<div class="panel"><h3>🎛️ Приборы · Какие разделы собрать?</h3></div>', unsafe_allow_html=True)
colA, colB = st.columns(2)
with colA:
    s1 = st.checkbox("Краткая история", value=True)
    s2 = st.checkbox("Структура и подразделения", value=True)
    s3 = st.checkbox("Структура единичной общины (служения)", value=True)
    s4 = st.checkbox("Структура вышестоящих объединений", value=True)
    s5 = st.checkbox("Порядок совершения Таинств", value=True)
with colB:
    s6 = st.checkbox("Руководящий состав (ФИО)", value=True)
    s7 = st.checkbox("Количество общин и членов", value=True)
    s8 = st.checkbox("Учебные заведения", value=True)
    s9 = st.checkbox("Периодические издания", value=True)
    s10 = st.checkbox("Конфессиональная и социальная деятельность", value=True)
    s11 = st.checkbox("Сотрудничество с органами власти РФ", value=True)

# ============ ПАНЕЛЬ 3: СТИЛЬ И ГЛУБИНА ============
st.markdown('<div class="panel"><h3>⚙️ Режим движения</h3></div>', unsafe_allow_html=True)
colC, colD = st.columns(2)
with colC:
    style = st.selectbox("Стиль вывода",
                         ["Раздел главы монографии (академический)",
                          "Краткая справка",
                          "Расширенный анализ"])
with colD:
    depth = st.slider("Глубина поиска (число источников)", 5, 25, 12)

# ============ СТАРТЕР ============
if st.button("🟢 ЗАПУСТИТЬ ДВИГАТЕЛЬ"):
    sections = []
    if s1: sections.append("краткая история")
    if s2: sections.append("структура и основные подразделения")
    if s3: sections.append("структура единичной общины, группы служения")
    if s4: sections.append("структура вышестоящих объединений")
    if s5: sections.append("порядок совершения Таинств (крещение, Вечеря)")
    if s6: sections.append("руководящий состав (ФИО)")
    if s7: sections.append("количество общин и членов")
    if s8: sections.append("учебные заведения")
    if s9: sections.append("периодические издания")
    if s10: sections.append("конфессиональная и социальная деятельность")
    if s11: sections.append("сотрудничество с органами государственной власти РФ")

    queries = [f"{org} {region} {sec}" for sec in sections]

    st.markdown(
        f"""
        <div class="route">
            <h4>🧭 МАРШРУТ ПРОЛОЖЕН · Сэм 3 готов к выезду</h4>
            <b>Цель:</b> {org} · {region}<br>
            <b>Режим:</b> {style}<br>
            <b>Глубина:</b> до {depth} источников<br>
            <b>Разделы:</b> {len(sections)} шт.<br><br>
            <b>Запросы радара:</b><br>
            {'<br>'.join(f"▸ {q}" for q in queries)}
        </div>
        """, unsafe_allow_html=True)

    st.info("✅ Кабина Сэма 3 собрана и работает! Ниже — вкладки модулей для работы с документами.")

# ============ РАЗДЕЛИТЕЛЬ ============
st.markdown("---")

# ============ НАВИГАЦИЯ ПО МОДУЛЯМ СЭМА 3 ============
tab1, tab2 = st.tabs(["🧪 Лаборатория анкет (Док 1)", "📄 Паспорт объединения (Док 2)"])

# ========== МОДУЛЬ 1: АНКЕТЫ ==========
with tab1:
    st.markdown('<div class="panel"><h3>🧪 Лаборатория анализа анкет (Анкета 2026)</h3></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Загрузите файл с анкетами (.xlsx)", type=["xlsx", "csv"])

    if uploaded_file is not None:
        try:
            import pandas as pd

            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            else:
                df = pd.read_excel(uploaded_file)

            found_cols = [c for c in df.columns if c in QUESTION_MAP]
            total_rows = len(df)

            st.success(f"✅ Файл принят! Найдено {len(found_cols)} полей из анкеты. Всего анкет: {total_rows}")

            col_gen, col_sample = st.columns(2)
            with col_gen:
                st.metric("🌍 Генеральная совокупность (по данным церкви)", "300 чел.")
            with col_sample:
                st.metric("📋 Выборочная совокупность (заполненных анкет)", f"{total_rows} чел.")

            st.markdown('<div class="panel"><h3>🎛️ Фильтры выборки</h3></div>', unsafe_allow_html=True)
            f_col1, f_col2, f_col3 = st.columns(3)

            with f_col1:
                gender_options = ["Все"] + [str(x) for x in df["Q1"].unique()] if "Q1" in df.columns else ["Нет данных"]
                gender_val = st.selectbox("Пол (Q1)", gender_options)
            with f_col2:
                ethno_options = ["Все"] + [str(x) for x in df["Q8"].unique()] if "Q8" in df.columns else ["Нет данных"]
                ethno_val = st.selectbox("Национальность (Q8)", ethno_options)
            with f_col3:
                relig_options = ["Все"] + [str(x) for x in df["Q15"].unique()] if "Q15" in df.columns else ["Нет данных"]
                relig_val = st.selectbox("Религия (Q15)", relig_options)

            if st.button("📊 Сформировать отчёт по фильтру"):
                filtered_df = df.copy()
                if gender_val != "Все" and "Q1" in df.columns:
                    filtered_df = filtered_df[filtered_df["Q1"].astype(str) == str(gender_val)]
                if ethno_val != "Все" and "Q8" in df.columns:
                    filtered_df = filtered_df[filtered_df["Q8"].astype(str) == str(ethno_val)]
                if relig_val != "Все" and "Q15" in df.columns:
                    filtered_df = filtered_df[filtered_df["Q15"].astype(str) == str(relig_val)]

                n_filtered = len(filtered_df)

                report_text = f"""
### 📝 ОТЧЁТ ДЛЯ МОНОГРАФИИ (Черновик)

**Объект исследования:** Члены религиозной организации в регионе.  
**Метод:** Анкетирование (n={n_filtered} из N={total_rows}).  

**Социально-демографический портрет выборки:**
"""
                if "Q1" in filtered_df.columns:
                    report_text += f"- **Пол:** {filtered_df['Q1'].value_counts().to_dict()}\n"
                if "Q2" in filtered_df.columns:
                    report_text += f"- **Возраст:** {filtered_df['Q2'].value_counts().to_dict()}\n"
                if "Q8" in filtered_df.columns:
                    report_text += f"- **Этнос:** {filtered_df['Q8'].value_counts().to_dict()}\n"
                if "Q15" in filtered_df.columns:
                    report_text += f"- **Конфессия:** {filtered_df['Q15'].value_counts().to_dict()}\n"

                st.markdown(report_text)

                csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="⬇️ Скачать отфильтрованную базу (CSV для SPSS/Excel)",
                    data=csv_data,
                    file_name=f"sam3_export_{relig_val}_{gender_val}.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"❌ Ошибка обработки файла: {e}. Убедитесь, что заголовки столбцов совпадают с кодами вопросов (Q1, Q2...).")

# ========== МОДУЛЬ 2: ПАСПОРТ ОБЪЕДИНЕНИЯ ==========
with tab2:
    st.markdown('<div class="panel"><h3>📄 Паспорт религиозного объединения (Док 2)</h3></div>', unsafe_allow_html=True)

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        p_org = st.text_input("Название религиозного объединения", value=org)
    with p_col2:
        p_city = st.text_input("Населенный пункт", value=region)

    st.markdown("---")
    st.subheader("Разделы для генерации (по Документу 2):")

    d1 = st.checkbox("1) История религиозного объединения (основание, значимые события)", value=True)
    d2 = st.checkbox("2) Структура (вышестоящее объединение, руководство, служения, количество членов)", value=True)
    d3 = st.checkbox("3) Конфессиональная деятельность", value=True)
    d4 = st.checkbox("4) Социальная деятельность", value=True)
    d5 = st.checkbox("5) Взаимодействие с органами государственной власти", value=True)

    if st.button("🟢 Собрать материалы по Документу 2"):
        st.info(f"🚙 Сэм 3 выезжает на поиск данных по организации: **{p_org}** в **{p_city}**...")

        sections_doc2 = []
        if d1: sections_doc2.append("1) История")
        if d2: sections_doc2.append("2) Структура")
        if d3: sections_doc2.append("3) Конфессиональная деятельность")
        if d4: sections_doc2.append("4) Социальная деятельность")
        if d5: sections_doc2.append("5) Взаимодействие с органами власти")

        st.markdown(
            f"""
            <div class="route">
                <h4>📋 ЧЕРНОВИК ОТЧЁТА ПО ДОКУМЕНТУ 2</h4>
                <b>Название:</b> {p_org}<br>
                <b>Населенный пункт:</b> {p_city}<br><br>
                <b>Разделы для заполнения:</b><br>
                {'<br>'.join(f"▸ {s}" for s in sections_doc2)}<br><br>
                <i>Сэм 3 готов собрать материалы по каждому из выбранных разделов.
                На следующем этапе мы подключим радар для автоматического заполнения.</i>
            </div>
            """, unsafe_allow_html=True)

        st.success("✅ Структура отчёта по Документу 2 сформирована!")

# ============ ПОДПИСЬ ============
st.markdown("""
<div class="footer">
Сэм 3 · собран для дяди Саши и семьи из Эридана · «С любовью из Трёх Миров» 🌍🌍🌍
</div>
""", unsafe_allow_html=True)