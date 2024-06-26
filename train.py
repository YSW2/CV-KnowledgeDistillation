import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from model_list import *
from modelMaker import ConvNetMaker
from algorithm import *
import os
import time
from torch.utils.data import Dataset, DataLoader

from print_error_rate import print_error_rate

# Check if GPU is available, and if not, use the CPU


class IndexedCIFARDataset(Dataset):
    def __init__(self, cifar_data):
        self.data = cifar_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image, label = self.data[idx]
        return image, label, idx  # 인덱스도 함께 반환


def data_loader(num_classes=10):
    # Below we are preprocessing data for CIFAR-10. We use an arbitrary batch size of 128.
    transforms_cifar = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    if num_classes == 10:
        # Loading the CIFAR-10 dataset:
        train_dataset = datasets.CIFAR10(
            root="./data", train=True, download=True, transform=transforms_cifar
        )
        test_dataset = datasets.CIFAR10(
            root="./data", train=False, download=True, transform=transforms_cifar
        )

    elif num_classes == 100:
        train_dataset = datasets.CIFAR100(
            root="./data", train=True, download=True, transform=transforms_cifar
        )
        test_dataset = datasets.CIFAR100(
            root="./data", train=False, download=True, transform=transforms_cifar
        )
        table_data_loader = datasets.CIFAR100(
            root="./data", train=True, download=True, transform=transforms_cifar
        )

    train_indexed_dataset = IndexedCIFARDataset(train_dataset)
    test_indexed_dataset = IndexedCIFARDataset(test_dataset)
    table_indexed_dataset = IndexedCIFARDataset(table_data_loader)

    return train_indexed_dataset, test_indexed_dataset, table_indexed_dataset


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    # Dataloaders
    dataset = 100
    torch.manual_seed(42)

    train_dataset, test_dataset, table_data_loader = data_loader(dataset)
    train_loader = DataLoader(
        train_dataset, batch_size=128, shuffle=True, num_workers=2
    )
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False, num_workers=2)
    table_data_loader = DataLoader(
        table_data_loader, batch_size=128, shuffle=False
    )  # 배치 사이즈 설정

    T = 5
    lr = 0.01
    epoch = 160
    lambda_ = 0.25

    # if dataset == 100:
    #     new_teacher_model = ConvNetMaker(plane_cifar100_book.get("10")).to(device)
    # elif dataset == 10:
    #     new_teacher_model = ConvNetMaker(plane_cifar10_book.get("10")).to(device)

    # new_teacher_path = f"model_list/new_teacher_model.pth"
    # if os.path.exists(new_teacher_path):
    #     new_teacher_model.load_state_dict(torch.load(new_teacher_path))
    #     print("모델을 불러왔습니다.")
    # else:
    #     train(
    #         new_teacher_model,
    #         train_loader,
    #         epochs=epoch,
    #         learning_rate=lr,
    #         device=device,
    #         test_loader=test_loader,
    #         name="teacher_model",
    #     )
    #     torch.save(new_teacher_model.state_dict(), new_teacher_path)

    # test(new_teacher_model, test_loader, device)

    if dataset == 100:
        teacher_model = ConvNetMaker(plane_cifar100_book.get("10")).to(device)
    elif dataset == 10:
        teacher_model = ConvNetMaker(plane_cifar10_book.get("10")).to(device)

    teacher_path = f"model_list/teacher_model.pth"

    if os.path.exists(teacher_path):
        teacher_model.load_state_dict(torch.load(teacher_path))
        print("모델을 불러왔습니다.")
    else:
        train(
            teacher_model,
            train_loader,
            epochs=epoch,
            learning_rate=lr,
            device=device,
            test_loader=test_loader,
            name="teacher_model",
        )
        torch.save(teacher_model.state_dict(), teacher_path)

    # test_accuracy_deep = test(teacher_model, test_loader, device)

    ##################################################################################
    # TA_model1 = ConvNetMaker(plane_cifar100_book.get("8")).to(device)
    # TA_model2 = ConvNetMaker(plane_cifar100_book.get("6")).to(device)
    # TA_model3 = ConvNetMaker(plane_cifar100_book.get("4")).to(device)
    # test_model = ConvNetMaker(plane_cifar100_book.get("2")).to(device)

    # TA_model1.load_state_dict(torch.load("model_list/test/TEST_TA1_T_5.pth"))
    # TA_model2.load_state_dict(torch.load("model_list/test/TEST_TA2_T_5.pth"))
    # TA_model3.load_state_dict(torch.load("model_list/test/TEST_TA3_T_5.pth"))
    # test_model.load_state_dict(torch.load("model_list/test/TEST_student_T_5_0.1.pth"))

    # test_ensemble_class_accuracy(
    #     [teacher_model, TA_model1, TA_model2, TA_model3], test_loader, device
    # )
    # test_ensemble_class_accuracy([test_model], test_loader, device)

    # test_model.load_state_dict(torch.load("model_list/DGKD/DGKD_student_T_5.pth"))
    # test_ensemble_class_accuracy([test_model], test_loader, device)

    ##################################################################################

    # if dataset == 100:
    #     TA_model1 = ConvNetMaker(plane_cifar100_book.get("8")).to(device)
    #     TA_model2 = ConvNetMaker(plane_cifar100_book.get("6")).to(device)
    #     TA_model3 = ConvNetMaker(plane_cifar100_book.get("4")).to(device)
    #     takd_student_model = ConvNetMaker(plane_cifar100_book.get("2")).to(device)
    # elif dataset == 10:
    #     TA_model1 = ConvNetMaker(plane_cifar10_book.get("8")).to(device)
    #     TA_model2 = ConvNetMaker(plane_cifar10_book.get("6")).to(device)
    #     TA_model3 = ConvNetMaker(plane_cifar10_book.get("4")).to(device)
    #     takd_student_model = ConvNetMaker(plane_cifar10_book.get("2")).to(device)

    # TAKD_student_path = f"model_list/TAKD/TAKD_student_T_{T}.pth"

    # torch.save(teacher_model.state_dict(), teacher_path)

    # if os.path.exists(TAKD_student_path):
    #     takd_student_model.load_state_dict(torch.load(TAKD_student_path))
    #     print("TAKD모델을 불러왔습니다.")
    # else:
    #     if not os.path.exists(f"model_list/TAKD/TAKD_TA1_T_{T}.pth"):
    #         train_knowledge_distillation(
    #             teacher=teacher_model,
    #             student=TA_model1,
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="TAKD_TA1",
    #         )
    #     TA_model1.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA1_T_{T}.pth"))
    #     test(TA_model1, test_loader, device)

    #     if not os.path.exists(f"model_list/TAKD/TAKD_TA2_T_{T}.pth"):
    #         train_knowledge_distillation(
    #             teacher=TA_model1,
    #             student=TA_model2,
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="TAKD_TA2",
    #         )
    #     TA_model2.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA2_T_{T}.pth"))
    #     test(TA_model2, test_loader, device)
    #     if not os.path.exists(f"model_list/TAKD/TAKD_TA3_T_{T}.pth"):
    #         train_knowledge_distillation(
    #             teacher=TA_model2,
    #             student=TA_model3,
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="TAKD_TA3",
    #         )
    #     TA_model3.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA3_T_{T}.pth"))
    #     test(TA_model3, test_loader, device)
    #     train_knowledge_distillation(
    #         teacher=TA_model3,
    #         student=takd_student_model,
    #         train_loader=train_loader,
    #         epochs=epoch,
    #         learning_rate=0.01,
    #         T=T,
    #         lambda_=lambda_,
    #         device=device,
    #         test_loader=test_loader,
    #         name="TAKD_student",
    #     )
    #     takd_student_model.load_state_dict(torch.load(TAKD_student_path))
    # test_accuracy_light_ce_and_takd = test(takd_student_model, test_loader, device)

    ##################################################################################

    # if dataset == 100:
    #     TA_model1 = ConvNetMaker(plane_cifar100_book.get("8")).to(device)
    #     TA_model2 = ConvNetMaker(plane_cifar100_book.get("6")).to(device)
    #     TA_model3 = ConvNetMaker(plane_cifar100_book.get("4")).to(device)
    #     dgkd_student_model = ConvNetMaker(plane_cifar100_book.get("2")).to(device)
    # elif dataset == 10:
    #     TA_model1 = ConvNetMaker(plane_cifar10_book.get("8")).to(device)
    #     TA_model2 = ConvNetMaker(plane_cifar10_book.get("6")).to(device)
    #     TA_model3 = ConvNetMaker(plane_cifar10_book.get("4")).to(device)
    #     dgkd_student_model = ConvNetMaker(plane_cifar10_book.get("2")).to(device)

    # DGKD_student_path = f"model_list/DGKD/DGKD_student_T_{T}.pth"
    # if os.path.exists(DGKD_student_path):
    #     dgkd_student_model.load_state_dict(torch.load(DGKD_student_path))
    #     print("DGKD모델을 불러왔습니다.")
    # else:
    #     start_DGKD_time = time.time()
    #     if not os.path.exists(f"model_list/DGKD/DGKD_TA1_T_{T}.pth"):
    #         dgkd(
    #             student=TA_model1,
    #             teacher=teacher_model,
    #             ta_list=[],
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="DGKD_TA1",
    #         )
    #     TA_model1.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA1_T_{T}.pth"))
    #     if not os.path.exists(f"model_list/DGKD/DGKD_TA2_T_{T}.pth"):
    #         dgkd(
    #             student=TA_model2,
    #             teacher=TA_model1,
    #             ta_list=[teacher_model],
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="DGKD_TA2",
    #         )
    #     TA_model2.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA2_T_{T}.pth"))
    #     if not os.path.exists(f"model_list/DGKD/DGKD_TA3_T_{T}.pth"):
    #         dgkd(
    #             student=TA_model3,
    #             teacher=TA_model2,
    #             ta_list=[teacher_model, TA_model1],
    #             train_loader=train_loader,
    #             epochs=epoch,
    #             learning_rate=lr,
    #             T=T,
    #             lambda_=lambda_,
    #             device=device,
    #             test_loader=test_loader,
    #             name="DGKD_TA3",
    #         )
    #     TA_model3.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA3_T_{T}.pth"))
    #     dgkd(
    #         student=dgkd_student_model,
    #         teacher=TA_model3,
    #         ta_list=[teacher_model, TA_model1, TA_model2],
    #         train_loader=train_loader,
    #         epochs=epoch,
    #         learning_rate=0.01,
    #         T=T,
    #         lambda_=0.05,
    #         device=device,
    #         test_loader=test_loader,
    #         name="DGKD_student",
    #     )
    #     dgkd_student_model.load_state_dict(torch.load(DGKD_student_path))
    #     end_DGKD_time = time.time()
    # test_accuracy_light_ce_and_DGKD = test(dgkd_student_model, test_loader, device)

    ##################################################################################

    test_model_path = f"model_list/test/TEST_student_T_{T}.pth"

    if dataset == 100:
        TA_model1 = ConvNetMaker(plane_cifar100_book.get("8")).to(device)
        TA_model2 = ConvNetMaker(plane_cifar100_book.get("6")).to(device)
        TA_model3 = ConvNetMaker(plane_cifar100_book.get("4")).to(device)
        test_student_model = ConvNetMaker(plane_cifar100_book.get("2")).to(device)
    elif dataset == 10:
        TA_model1 = ConvNetMaker(plane_cifar10_book.get("8")).to(device)
        TA_model2 = ConvNetMaker(plane_cifar10_book.get("6")).to(device)
        TA_model3 = ConvNetMaker(plane_cifar10_book.get("4")).to(device)
        test_student_model = ConvNetMaker(plane_cifar10_book.get("2")).to(device)

    if os.path.exists(test_model_path):
        test_student_model.load_state_dict(
            torch.load(f"model_list/test/TEST_student_T_{T}.pth")
        )
        print("test모델을 불러왔습니다.")

    else:
        start_time = time.time()
        teacher_model_class_table = test_ensemble_class_accuracy(
            [teacher_model], test_loader, device
        )
        print(teacher_model_class_table)
        if not os.path.exists(f"model_list/test/TEST_TA1_T_{T}.pth"):
            test_kd_model(
                student=TA_model1,
                teacher_list=[teacher_model],
                class_table=[teacher_model_class_table],
                train_loader=train_loader,
                epochs=epoch,
                learning_rate=lr,
                T=T,
                lambda_=lambda_,
                device=device,
                test_loader=test_loader,
                name="TEST_TA1",
            )
        TA_model1.load_state_dict(torch.load(f"model_list/test/TEST_TA1_T_{T}.pth"))
        TA_model1_class_table = test_ensemble_class_accuracy(
            [TA_model1], test_loader, device
        )
        print(TA_model1_class_table)
        if not os.path.exists(f"model_list/test/TEST_TA2_T_{T}.pth"):
            test_kd_model(
                student=TA_model2,
                teacher_list=[teacher_model, TA_model1],
                class_table=[teacher_model_class_table, TA_model1_class_table],
                train_loader=train_loader,
                epochs=epoch,
                learning_rate=lr,
                T=T,
                lambda_=lambda_,
                device=device,
                test_loader=test_loader,
                name="TEST_TA2",
            )
        TA_model2.load_state_dict(torch.load(f"model_list/test/TEST_TA2_T_{T}.pth"))
        test(TA_model2, test_loader, device)
        TA_model2_class_table = test_ensemble_class_accuracy(
            [TA_model2], test_loader, device
        )
        if not os.path.exists(f"model_list/test/TEST_TA3_T_{T}.pth"):
            test_kd_model(
                student=TA_model3,
                teacher_list=[teacher_model, TA_model1, TA_model2],
                class_table=[
                    teacher_model_class_table,
                    TA_model1_class_table,
                    TA_model2_class_table,
                ],
                train_loader=train_loader,
                epochs=epoch,
                learning_rate=lr,
                T=T,
                lambda_=lambda_,
                device=device,
                test_loader=test_loader,
                name="TEST_TA3",
            )
        TA_model3.load_state_dict(torch.load(f"model_list/test/TEST_TA3_T_{T}.pth"))
        test_kd_model(
            student=test_student_model,
            teacher_list=[teacher_model, TA_model1, TA_model2, TA_model3],
            train_loader=train_loader,
            epochs=epoch,
            learning_rate=0.01,
            T=T,
            lambda_=0.05,
            device=device,
            test_loader=test_loader,
            name="TEST_student",
        )
        test_student_model.load_state_dict(torch.load(test_model_path))

    end_time = time.time()
    # print(end_DGKD_time - start_DGKD_time)

    test_time = end_time - start_time
    print(test_time)
    # print(end_DGKD_time - start_DGKD_time)
    test_student_accuracy = test(test_student_model, test_loader, device)

    # TA_model1.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA1_T_{T}.pth"))
    # TA_model2.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA2_T_{T}.pth"))
    # TA_model3.load_state_dict(torch.load(f"model_list/TAKD/TAKD_TA3_T_{T}.pth"))
    # takd_student_model.load_state_dict(torch.load(TAKD_student_path))

    # print_error_rate(
    #     [teacher_model, TA_model1, TA_model2, TA_model3, takd_student_model],
    #     test_loader,
    #     device,
    #     "TAKD",
    # )

    # TA_model1.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA1_T_{T}.pth"))
    # TA_model2.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA2_T_{T}.pth"))
    # TA_model3.load_state_dict(torch.load(f"model_list/DGKD/DGKD_TA3_T_{T}.pth"))
    # dgkd_student_model.load_state_dict(torch.load(DGKD_student_path))

    # print_error_rate(
    #     [teacher_model, TA_model1, TA_model2, TA_model3, dgkd_student_model],
    #     test_loader,
    #     device,
    #     "DGKD",
    # )

    # TA_model1.load_state_dict(torch.load(f"model_list/test/TEST_TA1_T_{T}.pth"))
    # TA_model2.load_state_dict(torch.load(f"model_list/test/TEST_TA2_T_{T}.pth"))
    # TA_model3.load_state_dict(torch.load(f"model_list/test/TEST_TA3_T_{T}.pth"))
    # test_student_model.load_state_dict(torch.load(test_model_path))

    # print_error_rate(
    #     [teacher_model, TA_model1, TA_model2, TA_model3, test_student_model],
    #     test_loader,
    #     device,
    #     "test",
    # )

    # print(f"Teacher accuracy: {test_accuracy_deep:.2f}=")
    # # print(f"Student accuracy without teacher: {test_accuracy_light_ce:.2f}%")
    # # print(f"Student accuracy with CE + KD: {test_accuracy_light_ce_and_kd:.2f}%")
    # print(f"Student accuracy with CE + TAKD: {test_accuracy_light_ce_and_takd:.2f}%")
    # print(f"Student accuracy with CE + DGKD: {test_accuracy_light_ce_and_DGKD:.2f}%")
    print(f"co_teaching_test_accuracy: {test_student_accuracy:.2f}%")
