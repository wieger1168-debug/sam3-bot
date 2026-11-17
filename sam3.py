import streamlit as st
import os
import pandas as pd
from duckduckgo_search import DDGS

# ============ КАРТА ПАМЯТИ СЭМА 3 (СТРУКТУРА АНКЕТЫ 2026) ============
QUESTION_MAP = {
    "Q1": "Пол", "Q2": "Возраст", "Q3": "Место рождения", "Q4": "Где живёте",
    "Q5": "Семейное положение", "Q6": "Количество детей", "Q7": "Образование",
    "Q8": "Национальность", "Q9": "Язык обучения", "Q10": "Социальная группа",
    "Q11": "Статус", "Q12": "Личный доход", "Q13": "Семейный доход", "Q14": "Благосостояние",
    "Q15": "Текущая религия", "Q16": "Предыдущая религия", "Q17": "Год принятия религии",
    "Q18_1": "Идентичность 1-я", "Q18_2": "Идентичность 2-я", "Q18_3": "Идентичность 3-я",
    "Q18_4": "Идентичность 4-я", "Q18_5": "Идентичность 5-я", "Q19": "Место России в мире",
    "Q20": "Переориентация на Восток", "Q21": "Окружающая действительность",
    "Q22": "Процессы в России и мире", "Q23_1": "Электронные ресурсы: досуг",
    "Q23_2": "Электронные ресурсы: наука", "Q23_3": "Электронные ресурсы: альтернативные движения",
    "Q23_4": "Электронные ресурсы: религиозные", "Q24": "Чтение священных книг",
    "Q25": "Чтение религиозной литературы", "Q26": "Отношение к успеху",
    "Q27": "Литература о НРД", "Q28": "Мировое правительство / антихрист",
    "Q29": "Развитие IT-технологий", "Q30": "Определение брака", "Q31": "Отношение к деторождению",
    "Q32": "Отношение к абортам", "Q33_1": "Будущее РФ: СССР", "Q33_2": "Будущее РФ: Многополярность",
    "Q33_3": "Будущее РФ: Империя", "Q33_4": "Будущее РФ: Глобальный Запад", "Q33_5": "Будущее РФ: Восток",
    "Q34": "Отношение к Православию", "Q35": "Отношение к Исламу", "Q36": "Сотрудничество РО с государством",
    "Q37": "Частота посещения храма", "Q38": "Регулярность молитвы", "Q39": "Определение семьи",
    "Q40": "Тенденции развития человечества", "Q41": "Знание ФЗ о свободе совести",
    "Q42": "Соблюдение поста", "Q43": "Контроль гос-ва над РО", "Q44": "Отношение к Иудаизму",
    "Q45": "Отношение к НРД/оккультизму",
}

FILTER_KEYS = ["Q1", "Q2", "Q8", "Q15", "Q16", "Q34", "Q35", "Q44", "Q45"]

# ============ НАСТРОЙКИ СТРАНИЦЫ ============
st.set_page_config(page_title="СЭМ 3 — Вездеход по киберпространству", page_icon="🚙", layout="wide", initial_sidebar_state="collapsed")

# ============ СТИЛИ: ПРИБОРНАЯ ДОСКА СЭМА ============
st.markdown("""
<style>
    .stApp { background-color: #0b0f0b; color: #d8e6d8; }
    .windshield { background: linear-gradient(180deg, #1a3a1a 0%, #2e5a2e 40%, #4a7a3a 70%, #6b8f4a 100%); border: 3px solid #66ff66; border-radius: 12px; padding: 18px 24px; text-align: center; box-shadow: 0 0 25px rgba(102,255,102,0.35), inset 0 0 30px rgba(0,0,0,0.4); margin-bottom: 18px; }
    .windshield h1 { color: #eaffea; margin: 0; text-shadow: 2px 2px 6px #000; font-family: 'Courier New', monospace; letter-spacing: 3px; }
    .windshield p { color: #cfe8cf; margin: 6px 0 0 0; font-style: italic; }
    .panel { background: #111711; border: 2px solid #3a5a3a; border-radius: 10px; padding: 16px 20px; box-shadow: inset 0 0 12px rgba(0,0,0,0.6); }
    .panel h3 { color: #66ff66; font-family: 'Courier New', monospace; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px dashed #3a5a3a; padding-bottom: 6px; }
    .stTextInput input, .stSelectbox div, .stSlider div { background: #0e130e !important; color: #cfe8cf !important; border: 1px solid #3a5a3a !important; }
    .stCheckbox label { color: #d8e6d8 !important; }
    .stButton > button { background: linear-gradient(180deg, #2e7d32, #1b5e20); color: #eaffea; font-weight: bold; border: 2px solid #66ff66; border-radius: 8px; padding: 14px 30px; font-size: 18px; letter-spacing: 2px; box-shadow: 0 0 18px rgba(102,255,102,0.5); transition: all 0.2s; }
    .stButton > button:hover { background: linear-gradient(180deg, #388e3c, #2e7d32); box-shadow: 0 0 30px rgba(102,255,102,0.8); transform: scale(1.02); }
    .route { background: #060a06; border: 2px solid #1f4d1f; border-radius: 8px; padding: 16px; font-family: 'Courier New', monospace; color: #5fff5f; box-shadow: inset 0 0 18px rgba(0,255,0,0.15); }
    .route h4 { color: #aaffaa; margin-top: 0; }
    .footer { text-align: center; color: #6b8f6b; font-family: 'Courier New', monospace; font-size: 13px; margin-top: 24px; border-top: 1px dashed #2e4a2e; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ============ ЛОГОТИП СЭМА ============
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "sam_icon.png")
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True, caption="Сэм 3 · вид сбоку")
else:
    st.info("💡 Подсказка: положи файл sam_icon.png в папку с sam3.py — и Сэм появится в кабине!")

# ============ ШАПКА ============
st.markdown("""
<div class="windshield">
    <h1>🚙 СЭМ 3 · ВЕЗДЕХОД ПО КИБЕРПРОСТРАНСТВУ</h1>
    <p>«Ездит по сети так же уверенно, как Сэм 1 — по Ларамидии»</p>
</div>
""", unsafe_allow_html=True)

# ============ ПАНЕЛЬ 1: НАВИГАТОР ============
st.markdown('<div class="panel"><h3>🎯 Навигатор · Куда едем?</h3></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    org = st.text_input("Конфессиональная организация", value="РОСХВЕ", help="Например: РОСХВЕ, РЦХВЕ, ОЦХВЕ, РАНЦ ЕХБ, ХАСД РД")
with col2:
    region = st.text_input("Регион / территория", value="Воркутинский городской округ, Республика Коми", help="Город, район, область, край, республика")

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
    style = st.selectbox("Стиль вывода", ["Раздел главы монографии (академический)", "Краткая справка", "Расширенный анализ"])
with colD:
    depth = st.slider("Глубина поиска (число источников на раздел)", 3, 15, 5)

# ============ ФУНКЦИЯ РАДАРА (ПОИСК В ИНТЕРНЕТЕ) ============
def search_and_format(org, region, sections, depth):
    report = f"### {org} в регионе: {region}: историко-структурный и конфессиональный анализ\n\n"
    sources = []
    
    with st.spinner("🚙 Сэм 3 сканирует киберпространство..."):
        for sec in sections:
            report += f"**{sec.capitalize()}.** "
            query = f"{org} {region} {sec}"
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=depth))
                if results:
                    snippets = [r['body'] for r in results if 'body' in r]
                    # Формируем связный текст (ограничиваем объем, чтобы избежать "воды")
                    report += " ".join(snippets)[:1500] + "... "
                    for r in results:
                        if 'title' in r and 'href' in r:
                            sources.append(f"- {r['title']}. URL: {r['href']}")
                else:
                    report += "Данные в открытых источниках не найдены. "
            except Exception as e:
                report += f"Ошибка поиска: {str(e)}. "
            report += "\n\n"
            
        report += "### Список использованных источников и литературы\n"
        unique_sources = list(dict.fromkeys(sources)) # Убираем дубликаты
        for i, s in enumerate(unique_sources, 1):
            report += f"{i}. {s}\n"
            
    return report

# ============ СТАРТЕР ============
if st.button("🟢 ЗАПУСТИТЬ ДВИГАТЕЛЬ (Собрать данные)"):
    sections = []
    if s1: sections.append("краткая история")
    if s2: sections.append("структура и основные подразделения")
    if s3: sections.append("структура единичной общины, группы служения")
    if s4: sections.append("структура вышестоящих объединений")
    if s5: sections.append("порядок совершения Таинств")
    if s6: sections.append("руководящий состав")
    if s7: sections.append("количество общин и членов")
    if s8: sections.append("учебные заведения")
    if s9: sections.append("периодические издания")
    if s10: sections.append("конфессиональная и социальная деятельность")
    if s11: sections.append("сотрудничество с органами государственной власти РФ")

    if not sections:
        st.warning("⚠️ Пожалуйста, выберите хотя бы один раздел для сбора данных!")
    else:
        final_report = search_and_format(org, region, sections, depth)
        st.markdown('<div class="route"><h4>📝 ЧЕРНОВИК РАЗДЕЛА МОНОГРАФИИ</h4></div>', unsafe_allow_html=True)
        st.markdown(final_report)
        
        st.download_button(
            label="⬇️ Скачать черновик раздела (TXT)",
            data=final_report,
            file_name=f"Monograph_Section_{org}_{region}.txt",
            mime="text/plain"
        )

# ============ РАЗДЕЛИТЕЛЬ И ВКЛАДКИ ============
st.markdown("---")
tab1, tab2 = st.tabs(["🧪 Лаборатория анкет (Док 1)", "📄 Паспорт объединения (Док 2)"])

# ========== МОДУЛЬ 1: АНКЕТЫ ==========
with tab1:
    st.markdown('<div class="panel"><h3>🧪 Лаборатория анализа анкет (Анкета 2026)</h3></div>', unsafe_allow_html=True)
    # Поддерживаем xlsx, csv и docx (старый .doc не рекомендуется для облака)
    uploaded_file = st.file_uploader("Загрузите файл с анкетами (.xlsx, .csv или .docx)", type=["xlsx", "csv", "docx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".docx"):
            st.info("💡 Файл .docx загружен. Для статистического анализа Сэм 3 рекомендует использовать формат .xlsx или .csv, где каждый вопрос — это отдельный столбец (Q1, Q2...).")
        else:
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8-sig") if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                found_cols = [c for c in df.columns if c in QUESTION_MAP]
                st.success(f"✅ Файл принят! Найдено {len(found_cols)} полей из анкеты. Всего анкет: {len(df)}")
                
                f_col1, f_col2, f_col3 = st.columns(3)
                with f_col1:
                    g_opts = ["Все"] + [str(x) for x in df["Q1"].unique()] if "Q1" in df.columns else ["Нет данных"]
                    g_val = st.selectbox("Пол (Q1)", g_opts)
                with f_col2:
                    e_opts = ["Все"] + [str(x) for x in df["Q8"].unique()] if "Q8" in df.columns else ["Нет данных"]
                    e_val = st.selectbox("Национальность (Q8)", e_opts)
                with f_col3:
                    r_opts = ["Все"] + [str(x) for x in df["Q15"].unique()] if "Q15" in df.columns else ["Нет данных"]
                    r_val = st.selectbox("Религия (Q15)", r_opts)

                if st.button("📊 Сформировать отчёт по фильтру"):
                    f_df = df.copy()
                    if g_val != "Все" and "Q1" in df.columns: f_df = f_df[f_df["Q1"].astype(str) == str(g_val)]
                    if e_val != "Все" and "Q8" in df.columns: f_df = f_df[f_df["Q8"].astype(str) == str(e_val)]
                    if r_val != "Все" and "Q15" in df.columns: f_df = f_df[f_df["Q15"].astype(str) == str(r_val)]
                    
                    rpt = f"### 📝 ОТЧЁТ ДЛЯ МОНОГРАФИИ\n**Метод:** Анкетирование (n={len(f_df)}).\n**Портрет выборки:**\n"
                    for q in ["Q1", "Q2", "Q8", "Q15"]:
                        if q in f_df.columns: rpt += f"- **{QUESTION_MAP[q]}:** {f_df[q].value_counts().to_dict()}\n"
                    st.markdown(rpt)
                    st.download_button(label="⬇️ Скачать базу (CSV)", data=f_df.to_csv(index=False).encode('utf-8-sig'), file_name="sam3_export.csv", mime="text/csv")
            except Exception as e:
                st.error(f"❌ Ошибка: {e}. Убедитесь, что заголовки столбцов совпадают с кодами вопросов (Q1, Q2...).")

# ========== МОДУЛЬ 2: ПАСПОРТ ОБЪЕДИНЕНИЯ ==========
with tab2:
    st.markdown('<div class="panel"><h3>📄 Паспорт религиозного объединения (Док 2)</h3></div>', unsafe_allow_html=True)
    p_org = st.text_input("Название религиозного объединения", value=org)
    p_city = st.text_input("Населенный пункт", value=region)
    if st.button("🟢 Собрать материалы по Документу 2"):
        st.info(f"🚙 Сэм 3 использует данные из вкладки 'Радар' для заполнения структуры Документа 2 по организации: **{p_org}** в **{p_city}**.")
        st.success("✅ Используйте основную кнопку 'ЗАПУСТИТЬ ДВИГАТЕЛЬ' выше, выбрав соответствующие разделы, чтобы сформировать полный текст для Документа 2.")

# ============ ПОДПИСЬ ============
st.markdown("""
<div class="footer">
Сэм 3 · собран для дяди Саши и семьи из Эридана · «С любовью из Трёх Миров» 🌍🌍🌍
</div>
""", unsafe_allow_html=True)
