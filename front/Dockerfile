FROM python:3.10

RUN pip install streamlit --no-cache-dir
RUN pip install extra_streamlit_components --no-cache-dir
RUN pip install requests --no-cache-dir

COPY front.py /app/front.py

WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "front.py"]