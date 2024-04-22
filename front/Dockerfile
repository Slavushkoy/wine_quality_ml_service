FROM python:3.10

RUN pip install streamlit
RUN pip install extra_streamlit_components
RUN pip install requests

COPY front.py /app/front.py

WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "front.py"]