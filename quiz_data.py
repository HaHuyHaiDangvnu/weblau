"""Shared puzzle questions and answer validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellQuestion:
    clue: str
    choices: tuple[str, str, str, str]
    correct_choice: int


ANSWER = "HAPPYWOMEN'S"
QUESTIONS = (
    CellQuestion(
        "Theo nội dung bài học, khái niệm “Chất” được định nghĩa là gì?",
        (
            "Những đặc điểm có thể đo đếm hoặc xác định được của sự vật (như số lượng, quy mô, tốc độ).",
            "Tính quy định khách quan vốn có của sự vật, hiện tượng; là sự thống nhất hữu cơ các thuộc tính cơ bản làm cho sự vật là nó chứ không phải sự vật khác.",
            "Giới hạn mà trong đó sự thay đổi về lượng chưa làm thay đổi căn bản chất của sự vật.",
            "Giới hạn tại đó sự thay đổi về lượng phá vỡ độ cũ và dẫn đến sự thay đổi về chất.",
        ),
        1,
    ),
    CellQuestion(
        "Khái niệm “Lượng” dùng để chỉ điều gì?",
        (
            "Tính quy định khách quan biểu thị quy mô, số lượng, trình độ, nhịp điệu của sự vật.",
            "Những thuộc tính cơ bản làm cho sự vật khác với sự vật khác.",
            "Sự chuyển hóa căn bản từ sự vật này sang sự vật khác.",
            "Mâu thuẫn giữa các mặt đối lập trong sự vật.",
        ),
        0,
    ),
    CellQuestion(
        "“Độ” là khoảng giới hạn mà trong đó sự thay đổi về lượng như thế nào?",
        (
            "Làm chất của sự vật thay đổi ngay lập tức.",
            "Chưa làm thay đổi căn bản chất của sự vật.",
            "Chấm dứt sự tồn tại của sự vật.",
            "Làm xuất hiện một mâu thuẫn mới.",
        ),
        1,
    ),
    CellQuestion(
        "“Điểm nút” là gì trong quy luật chuyển hóa từ lượng thành chất?",
        (
            "Khoảng thời gian chất của sự vật được giữ ổn định.",
            "Sự thống nhất giữa các thuộc tính của sự vật.",
            "Thời điểm lượng tích lũy đã đủ làm thay đổi chất.",
            "Quá trình nhận thức sự vật bằng giác quan.",
        ),
        2,
    ),
    CellQuestion(
        "“Bước nhảy” là khái niệm chỉ điều gì?",
        (
            "Sự thay đổi dần dần về lượng trong giới hạn của độ.",
            "Sự chuyển hóa căn bản về chất của sự vật do lượng tích lũy đến điểm nút.",
            "Sự lặp lại nguyên trạng một sự vật.",
            "Sự đứng im tuyệt đối của sự vật.",
        ),
        1,
    ),
    CellQuestion(
        "Quy luật nào chỉ ra cách thức chung của sự phát triển?",
        (
            "Quy luật thống nhất và đấu tranh của các mặt đối lập.",
            "Quy luật phủ định của phủ định.",
            "Quy luật chuyển hóa từ những thay đổi về lượng thành những thay đổi về chất và ngược lại.",
            "Quy luật bảo toàn và chuyển hóa năng lượng.",
        ),
        2,
    ),
    CellQuestion(
        "Theo phép biện chứng duy vật, nguồn gốc của sự phát triển nằm ở đâu?",
        (
            "Tác động ngẫu nhiên từ bên ngoài sự vật.",
            "Mâu thuẫn bên trong sự vật, hiện tượng.",
            "Ý muốn chủ quan của con người.",
            "Sự đứng im và cân bằng tuyệt đối.",
        ),
        1,
    ),
    CellQuestion(
        "Hai mặt đối lập trong một mâu thuẫn biện chứng có quan hệ như thế nào?",
        (
            "Tách rời nhau và không tác động đến nhau.",
            "Chỉ thống nhất, không đấu tranh.",
            "Vừa thống nhất, vừa đấu tranh và chuyển hóa lẫn nhau trong điều kiện nhất định.",
            "Luôn triệt tiêu nhau ngay khi xuất hiện.",
        ),
        2,
    ),
    CellQuestion(
        "“Phủ định biện chứng” có đặc điểm nào?",
        (
            "Xóa bỏ hoàn toàn mọi yếu tố của cái cũ.",
            "Diễn ra khách quan và có tính kế thừa.",
            "Chỉ do ý muốn cá nhân quyết định.",
            "Làm sự vật quay về đúng trạng thái ban đầu.",
        ),
        1,
    ),
    CellQuestion(
        "Thực tiễn được hiểu là gì?",
        (
            "Hoạt động vật chất có mục đích, mang tính lịch sử - xã hội của con người.",
            "Suy nghĩ riêng của một cá nhân về thế giới.",
            "Mọi hoạt động tưởng tượng, không gắn với hiện thực.",
            "Tri thức có được mà không cần trải nghiệm.",
        ),
        0,
    ),
    CellQuestion(
        "Nhận thức cảm tính phản ánh sự vật chủ yếu bằng cách nào?",
        (
            "Thông qua khái niệm, phán đoán và suy luận.",
            "Thông qua cảm giác, tri giác và biểu tượng trực tiếp.",
            "Chỉ bằng các công thức toán học.",
            "Thông qua niềm tin không cần quan sát.",
        ),
        1,
    ),
    CellQuestion(
        "Nhận thức lý tính gồm những hình thức cơ bản nào?",
        (
            "Cảm giác, tri giác, biểu tượng.",
            "Quan sát, thí nghiệm, đo lường.",
            "Khái niệm, phán đoán, suy luận.",
            "Mục đích, phương tiện, kết quả.",
        ),
        2,
    ),
)


def validate_puzzle() -> None:
    if len(ANSWER) != 12 or len(QUESTIONS) != 12:
        raise ValueError("Trò chơi phải có đúng 12 ô và 12 câu hỏi.")
    for cell_number, question in enumerate(QUESTIONS, start=1):
        if len(question.choices) != 4:
            raise ValueError(f"Câu hỏi ô {cell_number} phải có đúng 4 đáp án.")
        if not 0 <= question.correct_choice < len(question.choices):
            raise ValueError(f"Đáp án đúng ở ô {cell_number} không hợp lệ.")
