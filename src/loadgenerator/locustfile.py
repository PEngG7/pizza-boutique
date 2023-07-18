import grpc
import time
from locust import TaskSet, User, between, task, events
from locust.exception import LocustError
from grpc_interceptor import ClientInterceptor
import demo_pb2
import demo_pb2_grpc
from typing import Any, Callable

class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environment

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            response_length = response.result().ByteSize()
        except grpc.RpcError as e:
            exception = e

        self.env.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )
        return response


class GrpcUsers(User):
    abstract = True
    stub_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel("trackingservice:50052")
        interceptor = LocustInterceptor(environment=self.environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = self.stub_class(self._channel)

class GrpcUser(TaskSet):
    @task
    def grpc_request(self):
        channel = grpc.insecure_channel("trackingservice:50052")
        self.stub = demo_pb2_grpc.TrackingServiceStub(channel)
        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6eyJjaXR5IjpbInN0cmluZyJdLCJjb3VudHJ5IjpbInN0cmluZyJdLCJuYW1lIjpbInN0cmluZyJdLCJwaG9uZSI6WyJzdHJpbmciXSwic3RyZWV0X25hbWUiOlsic3RyaW5nIl0sInN0cmVldF9udW1iZXIiOlsic3RyaW5nIl0sInppcF9jb2RlIjpbInN0cmluZyJdfSwiZ2VuZXJhbGl6ZWQiOnsiY3JlZGl0X2NhcmRfY3Z2IjpbImludCIsIjMiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl95ZWFyIjpbImludCIsIjEwIl0sImNyZWRpdF9jYXJkX251bWJlciI6WyJzdHJpbmciLCI1Il19LCJub2lzZWQiOnsiYWdlIjpbImludCIsIkxhcGxhY2UiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aCI6WyJpbnQiLCJMYXBsYWNlIl19LCJyZWR1Y2VkIjp7ImVtYWlsIjpbInN0cmluZyIsIjQiXX19LCJpc3MiOiJ0b2tlbkdlbmVyYXRvciIsImV4cCI6MTY4OTcwMTUzNn0.MXWdWqEIkCrM5QSbsAyIzT-lt6cX9KqPpWv8x_MaMMg8k6x7D8siQaMK2jp-cnVCBTkRFo_94euwnz1T5oI4Q4H5-ueiVxqWvzpGFa4mfCMmwf-xR1P9Xvfo04YO7QTfNrFStKCiukLKd5MT2R_nmsF-34auE3_-slLwvZz2lfRF7go6hqtih7YVOTIHNYHd82NPc-haqsqI8A_mjR6sGmNDuPsnXLq5NvIwBmLq5U6C3LVJxpgc63Y5ma7ACOXRSj4O3JqRN3xUpXyb5l38W2tRn4_FUtExvSLLxldzshuT1f4vRC6N0TT-M1RiPlyv60lshS7oYIm7Lt0mSa-4SQ'
        request_msg = demo_pb2.TrackingRequest(
            phone='030/1234567',
            street_name='Marchstr',
            street_number=23,
            zip_code=10383,
            city='Berlin',
            country='Germany',
            email='Test@mail.de',
            name='Mustermann',
            age=25
        )

        metadata = [('authorization', token)]

        response = self.stub.GetPersonaldata(request_msg, metadata=metadata)
        print(response)

class GrpcUser(GrpcUsers):
    stub_class = demo_pb2_grpc.TrackingServiceStub
    tasks = [GrpcUser]
    
