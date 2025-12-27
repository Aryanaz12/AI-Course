# ---------- کتابخونه‌های مورد نیاز ----------
import streamlit as st  # برای ساخت رابط کاربری وب ساده
from tmdbv3api import TMDb, Movie  # برای ارتباط با TMDb و گرفتن اطلاعات فیلم‌ها

# ---------- وصل شدن به TMDb ----------
tmdb = TMDb()  # ساختن آبجکت TMDb برای مدیریت ارتباط
tmdb.api_key = '8648392be269b4049bc33d20808eb6dd'  # <-- کلید API که از سایت TMDb گرفتی
movie_api = Movie()  # ساخت آبجکت Movie برای کار کردن با فیلم‌ها

# توضیح: 
# TMDb API به ما این امکان رو می‌ده که اطلاعات مربوط به فیلم‌ها، ژانرها، توضیحات،
# تاریخ انتشار، و فیلم‌های مشابه رو مستقیم از دیتابیس آنلاین بگیریم
# این یعنی لازم نیست خودمون دیتاست بسازیم و اطلاعات رو دستی وارد کنیم

# ---------- تنظیمات صفحه Streamlit ----------
st.set_page_config(page_title="Movie Recommendation Chatbot", layout="centered")
st.title("🎬 چت‌بات توصیه‌گر فیلم")  # عنوان بالای صفحه
st.write("اسم فیلم مورد علاقه‌ت رو وارد کن تا فیلم‌های مشابه برات پیشنهاد داده بشه:")

# ---------- گرفتن ورودی از کاربر ----------
user_input = st.text_input("نام فیلم:").strip()  # strip برای حذف فاصله اضافی اول و آخر

if user_input:
    # تبدیل ورودی به حروف کوچک برای اطمینان از اینکه حساس به حروف بزرگ/کوچک نشه
    user_input_lower = user_input.lower()  

    try:
        # ---------- جستجوی فیلم توی TMDb ----------
        search_result = movie_api.search(user_input)  
        # توضیح:
        # این خط از API استفاده می‌کنه و فیلم‌هایی که اسمشون شبیه ورودی کاربر هست رو برمی‌گردونه
        # search_result یک لیست از آبجکت‌های Movie هست، هر آبجکت شامل title, overview و ... است

        if search_result:
            m = search_result[0]  # اولین فیلمی که پیدا شد رو انتخاب می‌کنیم
            title = m.title
            description = m.overview if hasattr(m, 'overview') and m.overview else ''  
            # بررسی می‌کنیم که توضیح فیلم موجود باشه، در غیر اینصورت خالی می‌مونه

            # ---------- گرفتن فیلم‌های مشابه ----------
            similar_movies_obj = movie_api.similar(m.id)  
            # توضیح:
            # TMDb API یه متد مشابه هم داره که فیلم‌های شبیه فیلم موردنظر رو می‌تونه بده
            # اینجا m.id شناسه فیلم اصلی است که برای API ارسال می‌کنیم
            similar_movies = list(similar_movies_obj)  # تبدیل به لیست ساده برای راحتی استفاده

            # ---------- ساخت لیست پیشنهادی ----------
            recommendations = []
            for sm in similar_movies[:5]:  # فقط ۵ تا فیلم اول
                recommendations.append(sm.title)  # اسم فیلم مشابه رو اضافه می‌کنیم

            # ---------- نمایش خروجی به کاربر ----------
            st.write(f"فیلم‌هایی که شبیه **{title}** هستند:")
            for movie in recommendations:
                st.write("- " + movie)

        else:
            # اگر فیلمی پیدا نشد
            st.write("این فیلم در TMDb پیدا نشد. لطفاً اسم دقیق فیلم را وارد کن.")

    except Exception as e:
        # اگر خطایی در اتصال به TMDb یا گرفتن اطلاعات پیش آمد
        st.write("اوپس! یه مشکل پیش اومد تو ارتباط با TMDb API:", e)
        # توضیح:
        # این خطا می‌تونه به دلایل مختلف باشه مثل:
        # - اینترنت قطع بوده
        # - کلید API اشتباه بوده
        # - TMDb در دسترس نبوده