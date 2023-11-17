from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_validate_debit_card_valid():
    # 创建一个有效的借记卡信息
    valid_debit_card = {
        "card_number": "4147202464191053",
        "expiration_date": "12/25",
        "cvv": "123",
    }

    # 发送 POST 请求进行验证
    response = client.post("/debitCard", json=valid_debit_card)

    # 检查响应状态码是否为 201 (Created)
    assert response.status_code == 201

    # 检查响应 JSON 数据中的消息是否为 "Debit card is valid"
    assert response.json() == {"message": "Debit card is valid"}


def test_validate_debit_card_invalid():
    # 创建一个无效的借记卡信息
    invalid_debit_card = {
        "card_number": "1234567890123456",  # 无效的卡号
        "expiration_date": "05/22",
        "cvv": "abc",  # 无效的 CVV
    }

    # 发送 POST 请求进行验证
    response = client.post("/validate-debit-card", json=invalid_debit_card)

    # 检查响应状态码是否为 201 (Created)
    assert response.status_code == 201

    # 检查响应 JSON 数据中的消息是否为 "Debit card is invalid"
    assert response.json() == {"message": "Debit card is invalid"}
