import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='white')

st.header("E-commerce Orders Dashboard Dicoding")

def daily_orders(df):
    daily_orders_df = df.groupby(by='order_date').agg({
        'order_id':'nunique',
        'price':'sum'
    }).reset_index()

    return daily_orders_df

def category_orders(df):
    category_orders_df = df.groupby(by='category').agg({
        'order_id':'nunique',
        'price':'sum'
    }).reset_index()

    return category_orders_df

def category_rating_high(df):
    high_rating_df = df.groupby('category')['rating'].apply(lambda x: (x>3).mean()).sort_values(ascending=False).reset_index(name='rate')
    return high_rating_df

def category_rating_low(df):
    low_rating_df = df.groupby('category')['rating'].apply(lambda x: (x<3).mean()).sort_values(ascending=False).reset_index(name='rate')
    return low_rating_df

all_df = pd.read_csv('data_ecommerce.csv')

datetime_columns = ["order_date", "review_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df['order_date'].min()
max_date = all_df['order_date'].max()

col1, col2, col3 = st.columns(3)

with col3:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df['order_date'] >= str(start_date)) &
                 (all_df['order_date'] <= str(end_date))]

daily_orders_df = daily_orders(main_df)
category_df = category_orders(main_df)
high_rate = category_rating_high(main_df)
low_rate = category_rating_low(main_df)

color_high = ["#064ACB", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
color_low = ["#F3A953", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

with col1:
    total_orders = daily_orders_df.order_id.sum()
    st.metric('Total Orderan', value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.price.sum(), 'USD', locale='es_CO')
    st.metric('Total Pendapatan', value=total_revenue)

############# Performa Penjualan #############
st.subheader("Penjualan Harian")

fig, ax =plt.subplots(figsize=(20,8))
ax.plot(daily_orders_df['order_date'],
        daily_orders_df['order_id'],
        marker='o',
        linewidth=2)
ax.set_title('Jumlah Order', fontsize=30)
ax.set_ylabel('orders', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax =plt.subplots(figsize=(20,8))
ax.plot(daily_orders_df['order_date'],
        daily_orders_df['price'],
        marker='o',
        linewidth=2,
        color='orange')
ax.set_title('Jumlah Pendapatan', fontsize=30)
ax.set_ylabel('US$', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

############# Penjualan Kategori Produk #############
st.subheader("Penjualan Kategori Produk")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

sns.barplot(x='order_id', y='category', data=category_df.sort_values(by='order_id', ascending=False)[:5], ax=ax[0], palette=color_high)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Terjual", fontsize=40)
ax[0].set_title("Penjualan Terbanyak", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x='order_id', y='category', data=category_df.sort_values(by='order_id', ascending=True)[:5], ax=ax[1], palette=color_low)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Terjual", fontsize=40)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Penjualan Terendah", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

############# Rating Kategori Produk #############
st.subheader("Rating Kategori Produk")

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,5))

sns.barplot(x='rate', y='category', data=high_rate[:5].sort_values('rate', ascending=False), ax=ax[0], palette=color_high)
ax[0].set_title("Rating Tinggi Terbanyak")
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)

sns.barplot(x='rate', y='category', data=low_rate[:5].sort_values('rate', ascending=False), ax=ax[1], palette=color_low)
ax[1].set_title("Rating Rendah Terbanyak")
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)

fig.subplots_adjust(hspace=0.5)
st.pyplot(fig)

st.caption('Copyright (c) by Eko Rahmat 2023')
