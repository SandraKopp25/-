FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/
WORKDIR /service/marketplace
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I /service/protobufs --python_out=. --grpc_python_out=. /service/protobufs/recommendations.proto

EXPOSE 50051
ENV FLASK App=marketplace.py
ENTRYPOINT [ "python", "marketplace.py" ]