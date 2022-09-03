#python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto

python -m grpc_tools.protoc -I../../ -I. --python_out=. --grpc_python_out=. .\user.proto