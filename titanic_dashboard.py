import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ladataan Titanic-data
@st.cache_data
def load_data():
    file_path = r"D:\Koulu\Low-Code\Tehtävä 4\Titanic Data.xlsx"
    df = pd.read_excel(file_path, sheet_name="Titanic-Dataset")
    return df

data = load_data()

# Otsikko
st.title("🚢 Titanic Data Dashboard")

# Sivupalkki (Asetukset)
st.sidebar.header("⚙️ Asetukset")

# Ikärajain (slider)
age_range = st.sidebar.slider("Valitse ikähaarukka:", int(data["Age"].min()), int(data["Age"].max()), (10, 50))
filtered_data = data[(data["Age"] >= age_range[0]) & (data["Age"] <= age_range[1])]

# Käytetään containeria rakenteen selkeyttämiseen
with st.container():
    st.header("🧑‍🤝‍🧑 Sukupuolijakauma")
    fig, ax = plt.subplots()
    filtered_data['Sex'].value_counts().plot(kind='bar', color=['blue', 'pink'], ax=ax)
    ax.set_ylabel("Määrä")
    ax.set_xlabel("Sukupuoli")
    ax.set_title("Matkustajien sukupuolijakauma")
    st.pyplot(fig)

    st.header("🎟️ Matkustajaluokat")
    selected_class = st.selectbox("Valitse matkustajaluokka:", ["Kaikki"] + list(data['Pclass'].unique()))
    if selected_class != "Kaikki":
        filtered_data = filtered_data[filtered_data['Pclass'] == selected_class]

    fig, ax = plt.subplots()
    filtered_data['Pclass'].value_counts().sort_index().plot(kind='bar', ax=ax)
    ax.set_ylabel("Määrä")
    ax.set_xlabel("Luokka")
    ax.set_title("Matkustajaluokan jakauma")
    st.pyplot(fig)

# Selviytymisaste
st.header("⚰️ Selviytymisaste")
survival_rate = filtered_data['Survived'].value_counts(normalize=True) * 100
st.write(f"Selviytyneiden osuus: **{survival_rate.get(1, 0):.2f}%**")

fig, ax = plt.subplots()
survival_rate.plot(kind='bar', color=['red', 'green'], ax=ax)
ax.set_ylabel("%")
ax.set_xticklabels(["Ei selvinnyt", "Selvinnyt"], rotation=0)
ax.set_title("Selviytymisaste")
st.pyplot(fig)

# Ikäjakauma
st.header("📊 Ikäjakauma")
fig, ax = plt.subplots()
filtered_data['Age'].hist(bins=30, edgecolor='black', ax=ax)
ax.set_xlabel("Ikä")
ax.set_ylabel("Määrä")
ax.set_title("Ikäjakauma")
st.pyplot(fig)

# Mahdollisuus ladata suodatettu CSV-tiedosto
st.write("Voit ladata suodatetun Titanic-datan CSV-muodossa:")
st.download_button("📥 Lataa CSV", filtered_data.to_csv(index=False), "titanic_filtered.csv", "text/csv")
