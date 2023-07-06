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
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"

	purposelimiter "github.com/louisloechel/jwt-go-purposelimiter"

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
		//srv = grpc.NewServer()
		srv = grpc.NewServer(grpc.UnaryInterceptor(purposelimiter.UnaryServerInterceptor()))
	} else {
		log.Info("Stats disabled.")
		//srv = grpc.NewServer()
		srv = grpc.NewServer(grpc.UnaryInterceptor(purposelimiter.UnaryServerInterceptor()))
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
		// Pd: &pb.PersonalData{
		// 	Phone: in.Phone,
		// 	Address: in.Address,
		// 	Email: in.Email,
		// 	Lastname: in.Lastname,
		// 	CreditCard: in.CreditCard,
		// 	Birthdate: in.Birthdate,
		// },
		Phone:      in.Phone,
		Address:    in.Address,
		Email:      in.Email,
		Lastname:   in.Lastname,
		CreditCard: in.CreditCard,
		Birthdate:  in.Birthdate,
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

// type CustomClaims struct {
// 	Policy struct {
// 		Allowed     map[string]string `json:"allowed"`
// 		Generalized map[string]string `json:"generalized"`
// 		Noised      map[string]string `json:"noised"`
// 		Reduced     map[string]string `json:"reduced"`
// 	} `json:"policy"`

// 	jwt.StandardClaims
// }

// func UnaryServerInterceptor() grpc.UnaryServerInterceptor {
// 	return interceptor
// }

// func interceptor(
// 	ctx context.Context,
// 	req interface{},
// 	info *grpc.UnaryServerInfo,
// 	handler grpc.UnaryHandler,
// ) (interface{}, error) {

// 	h, err := handler(ctx, req)
// 	if err != nil {
// 		return nil, err
// 	}

// 	if md, ok := metadata.FromIncomingContext(ctx); ok {
// 		if token := md.Get("authorization"); len(token) > 0 {
// 			tkn, err := jwt.ParseWithClaims(token[0], &CustomClaims{}, func(token *jwt.Token) (interface{}, error) {
// 				return []byte(""), nil
// 			})

// 			// -------------------------
// 			// ! Validation not working !
// 			// -------------------------

// 			if err != nil {
// 				// return nil, err
// 			}

// 			if !tkn.Valid {
// 				// return nil, jwt.NewValidationError("token is invalid", jwt.ValidationErrorMalformed)
// 			}

// 			claims, ok := tkn.Claims.(*CustomClaims)
// 			if !ok {
// 				// return nil, jwt.NewValidationError("claims are not valid", jwt.ValidationErrorMalformed)
// 			}

// 			if claims.StandardClaims.VerifyIssuer("test", true) {
// 				// return nil, jwt.NewValidationError("issuer is invalid", jwt.ValidationErrorMalformed)
// 			}

// 			if claims.StandardClaims.VerifyExpiresAt(time.Now().Unix(), true) {
// 				// return nil, jwt.NewValidationError("token is expired", jwt.ValidationErrorExpired)
// 			}

// 			// -------------------------
// 			// ! Validation not working !
// 			// -------------------------

// 			// Check if the response is a proto.Message
// 			fmt.Println("ZZZZZZZZZZZZZZZZZZ")
// 			fmt.Println(h)
// 			msg, _ := h.(proto.Message)
// 			if !ok {
// 				return nil, fmt.Errorf("response is not a proto.Message")
// 			}

// 			// Invoke ProtoReflect() to get a protoreflect.Message
// 			reflectedMsg := msg.ProtoReflect()

// 			// Declare a slice to store field names
// 			var fieldNames []string

// 			reflectedMsg.Range(func(fd protoreflect.FieldDescriptor, v protoreflect.Value) bool {

// 				name := fd.TextName()
// 				fieldNames = append(fieldNames, name)

// 				return true
// 			})

// 			// Iterate over the fields of the message
// 			for _, field := range fieldNames {
// 				// Check if the field is in the allowed list
// 				if !contains(claims.Policy.Allowed, field) {
// 					// Check if the field is in one of the minimized lists
// 					if contains(claims.Policy.Generalized, field) {
// 						// Generalize the field
// 						switch reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)).Kind() {
// 						case protoreflect.Int32Kind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(generalizeInt(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).Int())))
// 						case protoreflect.StringKind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(generalizeString(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).String())))
// 						}
// 					} else if contains(claims.Policy.Noised, field) {
// 						// Noise the field
// 						switch reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)).Kind() {
// 						case protoreflect.Int32Kind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(noiseInt(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).Int())))
// 						case protoreflect.StringKind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(noiseString(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).String())))
// 						}
// 					} else if contains(claims.Policy.Reduced, field) {
// 						// Reduce the field
// 						switch reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)).Kind() {
// 						case protoreflect.Int32Kind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(reduceInt(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).Int())))
// 						case protoreflect.StringKind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(reduceString(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).String())))
// 						}
// 					} else {
// 						//Suppress the field
// 						switch reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)).Kind() {
// 						case protoreflect.Int32Kind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(suppressInt(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).Int())))
// 						case protoreflect.StringKind:
// 							reflectedMsg.Set(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field)), protoreflect.ValueOf(suppressString(reflectedMsg.Get(reflectedMsg.Descriptor().Fields().ByName(protoreflect.Name(field))).String())))
// 						}
// 					}
// 				}
// 			}
// 		}
// 	}

// 	return h, nil
// }

// // ------ minimzation functions ------

// // Suppression functions
// func suppressInt(number int64) int32 {
// 	// receives an integer (e.g., house number) and returns -1 as "none".
// 	return -1
// }
// func suppressString(text string) string {
// 	// receives a string (e.g., street name) and cuts it off after the 5th character.
// 	return ""
// }

// // Noising functions
// func noiseInt(number int64) int64 {
// 	// receives a house number and returns noised version of it.
// 	// rand.Int31 returns a non-negative pseudo-random 31-bit integer as an int32 from the default Source.
// 	return number - rand.Int63n(number) + rand.Int63n(number)
// }
// func noiseString(string) string {
// 	// receives a string and returns noised version of it.
// 	return ""
// }

// // Generalization functions
// func generalizeInt(number int64) int64 {
// 	// receives an integer (e.g., house number) and returns its range of 10's as the lower end of the interval.
// 	// e.g. 135 -> 131
// 	return number/10*10 + 1
// }
// func generalizeString(text string) string {
// 	// receives a string (e.g., street name) and returns the first character.
// 	return text[0:1]
// }

// // Reduction functions
// func reduceInt(number int64) int64 {
// 	return number / 10
// }

// func reduceString(text string) string {
// 	// receives a string (e.g., street name) and returns the first 4 characters.
// 	return text[0:3]
// }

// // ------ utiliy functions ------

// // contains checks if a field is present in a map
// func contains(m map[string]string, key string) bool {
// 	_, ok := m[key]
// 	return ok
// }
