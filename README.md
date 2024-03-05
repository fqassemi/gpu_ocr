This is a simple template fastAPI app to start and stop https://fluidstack.io server. 
I first create a server and install desired libraries. Here, I installed nougat ocr (https://github.com/facebookresearch/nougat). 
One can simply test this using the following API:
# API call
<code>curl -X 'POST'   'https://llms-xyz.tech/gpu_ocr'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'file=@</path/to/pdf>;type=application/pdf' -m 200
</code>
