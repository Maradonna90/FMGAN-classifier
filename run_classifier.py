import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

#GENERAL PARAMETERS
input_size = 224

#NUMBER OF CLASSES
num_classes = 9
#DATA_DIR
data_dir = '/content/drive/My Drive/stylegan2-colab/stylegan2/results/00003-generate-images'

#CHECK FOR GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# TRANSFORMATIONS
transform = transforms.Compose(
    [transforms.Resize(input_size),
    transforms.ToTensor(),
     transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

#DEFINE DATA
testset = torchvision.datasets.ImageFolder(data_dir, transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)



# LOAD MODEL
PATH = './FMGAN_net.pth'
model = models.vgg16(pretrained=True)
model.classifier[6] = nn.Linear(4096, num_classes)
model.load_state_dict(torch.load(PATH))
model.eval()

#TRANSFORM TO CUDA
model.to(device)

#RUNNING
with torch.no_grad():
    for data in testloader:
        inputs, labels = data[0].to(device), data[1].to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        print(predicted)
        break
#TODO: sort dataset

