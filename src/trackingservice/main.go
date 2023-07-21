// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"context"
	"fmt"
	"net"
	"os"
	"time"

	"cloud.google.com/go/profiler"
	purposelimiter "github.com/louisloechel/purpl"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"

	//naive "github.com/PEngG7/naive-approach"

	// "github.com/golang-jwt/jwt"
	// "google.golang.org/grpc/metadata"
	// "google.golang.org/protobuf/proto"
	// "google.golang.org/protobuf/reflect/protoreflect"

	//"github.com/Siar-Akbayin/jwt-go-auth"

	pb "github.com/GoogleCloudPlatform/microservices-demo/src/shippingservice/genproto"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
)

const (
	defaultPort = "50052"
)

var log *logrus.Logger

func init() {
	log = logrus.New()
	log.Level = logrus.DebugLevel
	log.Formatter = &logrus.JSONFormatter{
		FieldMap: logrus.FieldMap{
			logrus.FieldKeyTime:  "timestamp",
			logrus.FieldKeyLevel: "severity",
			logrus.FieldKeyMsg:   "message",
		},
		TimestampFormat: time.RFC3339Nano,
	}
	log.Out = os.Stdout
}

func main() {
	if os.Getenv("DISABLE_TRACING") == "" {
		log.Info("Tracing enabled, but temporarily unavailable")
		log.Info("See https://github.com/GoogleCloudPlatform/microservices-demo/issues/422 for more info.")
		go initTracing()
	} else {
		log.Info("Tracing disabled.")
	}

	if os.Getenv("DISABLE_PROFILER") == "" {
		log.Info("Profiling enabled.")
		go initProfiling("trackingservice", "1.0.0")
	} else {
		log.Info("Profiling disabled.")
	}

	port := defaultPort
	if value, ok := os.LookupEnv("PORT"); ok {
		port = value
	}
	port = fmt.Sprintf(":%s", port)

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	var srv *grpc.Server
	if os.Getenv("DISABLE_STATS") == "" {
		log.Info("Stats enabled, but temporarily unavailable")
		// Baseline - No Interceptor at all
		//srv = grpc.NewServer()

		// No-Op Interceptor
		//srv = grpc.NewServer(grpc.UnaryInterceptor(UnaryServerInterceptor()))

		// Our purposelimiter interceptor
		srv = grpc.NewServer(grpc.UnaryInterceptor(purposelimiter.UnaryServerInterceptor("key.pem")))

		// naive monolithic approach
		//srv = grpc.NewServer(grpc.UnaryInterceptor(naive.UnaryServerInterceptor("policy.json", "trackingService-maximal", "purpose1", "key_private.pem", "public.pem")))
	} else {
		log.Info("Stats disabled.")
		// Baseline - No Interceptor at all
		//srv = grpc.NewServer()

		// No-Op Interceptor
		//srv = grpc.NewServer(grpc.UnaryInterceptor(UnaryServerInterceptor()))

		// Our purposelimiter interceptor
		srv = grpc.NewServer(grpc.UnaryInterceptor(purposelimiter.UnaryServerInterceptor("key.pem")))

		// naive monolithic approach
		//srv = grpc.NewServer(grpc.UnaryInterceptor(naive.UnaryServerInterceptor("policy.json", "trackingService-maximal", "purpose1", "key_private.pem", "public.pem")))
	}
	svc := &server{}
	pb.RegisterTrackingServiceServer(srv, svc)
	healthpb.RegisterHealthServer(srv, svc)
	log.Infof("Tracking Service listening on port %s", port)

	// Register reflection service on gRPC server.
	reflection.Register(srv)
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

// server controls RPC service responses.
type server struct{}

// Check is for health checking.
func (s *server) Check(ctx context.Context, req *healthpb.HealthCheckRequest) (*healthpb.HealthCheckResponse, error) {
	return &healthpb.HealthCheckResponse{Status: healthpb.HealthCheckResponse_SERVING}, nil
}

func (s *server) Watch(req *healthpb.HealthCheckRequest, ws healthpb.Health_WatchServer) error {
	return status.Errorf(codes.Unimplemented, "health check via Watch not implemented")
}

func (s *server) GetPersonaldata(ctx context.Context, in *pb.TrackingRequest) (*pb.TrackingResponse, error) {
	log.Info("[GetPersonaldata] received request")
	defer log.Info("[GetPersonaldata] completed request")

	return &pb.TrackingResponse{
		Phone:                     in.Phone,
		StreetName:                in.StreetName,
		StreetNumber:              in.StreetNumber,
		ZipCode:                   in.ZipCode,
		City:                      in.City,
		Country:                   in.Country,
		Email:                     in.Email,
		Name:                      in.Name,
		CreditCardNumber:          in.CreditCardNumber,
		CreditCardCvv:             in.CreditCardCvv,
		CreditCardExpirationYear:  in.CreditCardExpirationYear,
		CreditCardExpirationMonth: in.CreditCardExpirationMonth,
		Age:                       in.Age,
		// Phone2:                     in.Phone2,
		// StreetName2:                in.StreetName2,
		// StreetNumber2:              in.StreetNumber2,
		// ZipCode2:                   in.ZipCode2,
		// City2:                      in.City2,
		// Country2:                   in.Country2,
		// Email2:                     in.Email2,
		// Name2:                      in.Name2,
		// CreditCardNumber2:          in.CreditCardNumber2,
		// CreditCardCvv2:             in.CreditCardCvv2,
		// CreditCardExpirationYear2:  in.CreditCardExpirationYear2,
		// CreditCardExpirationMonth2: in.CreditCardExpirationMonth2,
		// Age2:                       in.Age2,
		// Phone3:                     in.Phone3,
		// StreetName3:                in.StreetName3,
		// StreetNumber3:              in.StreetNumber3,
		// ZipCode3:                   in.ZipCode3,
		// City3:                      in.City3,
		// Country3:                   in.Country3,
		// Email3:                     in.Email3,
		// Name3:                      in.Name3,
		// CreditCardNumber3:          in.CreditCardNumber3,
		// CreditCardCvv3:             in.CreditCardCvv3,
		// CreditCardExpirationYear3:  in.CreditCardExpirationYear3,
		// CreditCardExpirationMonth3: in.CreditCardExpirationMonth3,
		// Age3:                       in.Age3,
		// Phone4:                     in.Phone4,
		// StreetName4:                in.StreetName4,
		// StreetNumber4:              in.StreetNumber4,
		// ZipCode4:                   in.ZipCode4,
		// City4:                      in.City4,
		// Country4:                   in.Country4,
		// Email4:                     in.Email4,
		// Name4:                      in.Name4,
		// CreditCardNumber4:          in.CreditCardNumber4,
		// CreditCardCvv4:             in.CreditCardCvv,
		// CreditCardExpirationYear4:  in.CreditCardExpirationYear4,
		// CreditCardExpirationMonth4: in.CreditCardExpirationMonth4,
		// Age4:                       in.Age4,
	}, nil
}

func initStats() {
	//TODO(arbrown) Implement OpenTelemetry stats
}

func initTracing() {
	// TODO(arbrown) Implement OpenTelemetry tracing
}

func initProfiling(service, version string) {
	// TODO(ahmetb) this method is duplicated in other microservices using Go
	// since they are not sharing packages.
	for i := 1; i <= 3; i++ {
		if err := profiler.Start(profiler.Config{
			Service:        service,
			ServiceVersion: version,
			// ProjectID must be set if not running on GCP.
			// ProjectID: "my-project",
		}); err != nil {
			log.Warnf("failed to start profiler: %+v", err)
		} else {
			log.Info("started Stackdriver profiler")
			return
		}
		d := time.Second * 10 * time.Duration(i)
		log.Infof("sleeping %v to retry initializing Stackdriver profiler", d)
		time.Sleep(d)
	}
	log.Warn("could not initialize Stackdriver profiler after retrying, giving up")
}

func UnaryServerInterceptor() grpc.UnaryServerInterceptor {
	return interceptor
}

func interceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {

	h, _ := handler(ctx, req)
	return h, nil
}
