import paddle

print("Is CUDA available?:", paddle.is_compiled_with_cuda())
print("Current device:", paddle.device.get_device())
