"""Trò chơi mở khóa 12 chữ cái bằng câu hỏi trắc nghiệm."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox

from PIL import Image, ImageOps, ImageTk


@dataclass(frozen=True)
class CellQuestion:
    clue: str
    choices: tuple[str, str, str, str]
    correct_choice: int

ANSWER = "HAPPYWOMEN'S"
APP_BACKGROUND = "#245b98"
PAGE_BACKGROUND = "white"
BUTTON_BACKGROUND = "#006bb3"
BORDER_COLOR = "#7dd3fc"
ACTIVE_BORDER_COLOR = "#0ea5e9"
WRONG_BACKGROUND = "#dc2626"
CORRECT_BACKGROUND = "#16a34a"
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

"""Phần kiểm tra tính hợp lệ của trò chơi"""
def validate_puzzle() -> None:
    if len(ANSWER) != 12 or len(QUESTIONS) != 12:
        raise ValueError("Trò chơi phải có đúng 12 ô và 12 câu hỏi.")
    for cell_number, question in enumerate(QUESTIONS, start=1):
        if len(question.choices) != 4:
            raise ValueError(f"Câu hỏi ô {cell_number} phải có đúng 4 đáp án.")
        if not 0 <= question.correct_choice < len(question.choices):
            raise ValueError(f"Đáp án đúng ở ô {cell_number} không hợp lệ.")


class CrosswordGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Trò chơi 12 câu hỏi trắc nghiệm")
        self.root.geometry("1100x900")
        self.root.minsize(900, 760)
        self.root.configure(bg=APP_BACKGROUND)
        self.background_canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bd=0,
        )
        self.background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_draw_pending = False
        self.root.bind("<Configure>", self._queue_background_draw)

        self.revealed: set[int] = set()
        self.question_labels: list[tk.Label] = []
        self.cell_buttons: list[tk.Button] = []
        self.active_cell: int | None = None
        self.selected_choice = tk.IntVar(value=-1)
        self.question_title_var = tk.StringVar(
            value="Chọn một số phía trên để xem câu hỏi."
        )
        self.feedback_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Chọn một số để trả lời câu hỏi!")
        self.completion_announced = False
        self.completion_image: ImageTk.PhotoImage | None = None
        self.completion_image_path = str(
            Path(__file__).resolve().parent
            / "assets"
            / "chuc_mung_20_10.png"
        )
        self.question_choices: list[tk.Frame] = []
        self.choice_text_labels: list[tk.Label] = []
        self.choice_badges: list[tk.Label] = []
        self.question_title_label: tk.Label

        self._build_interface()

    def _queue_background_draw(self, event: tk.Event) -> None:
        if event.widget is not self.root or self.background_draw_pending:
            return

        self.background_draw_pending = True
        self.root.after_idle(self._draw_background)

    def _draw_background(self) -> None:
        self.background_draw_pending = False
        width = max(1, self.root.winfo_width())
        height = max(1, self.root.winfo_height())
        columns = 40
        rows = 40
        top_left = (23, 107, 169)
        top_right = (38, 84, 155)
        bottom_left = (34, 93, 160)
        bottom_right = (47, 68, 146)

        self.background_canvas.delete("gradient")
        for row in range(rows):
            y = row / max(1, rows - 1)
            for column in range(columns):
                x = column / max(1, columns - 1)
                color = tuple(
                    round(
                        top_left[channel] * (1 - x) * (1 - y)
                        + top_right[channel] * x * (1 - y)
                        + bottom_left[channel] * (1 - x) * y
                        + bottom_right[channel] * x * y
                    )
                    for channel in range(3)
                )
                fill = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                self.background_canvas.create_rectangle(
                    column * width / columns,
                    row * height / rows,
                    (column + 1) * width / columns + 1,
                    (row + 1) * height / rows + 1,
                    fill=fill,
                    outline=fill,
                    tags="gradient",
                )

    def _build_interface(self) -> None:
        header = tk.Frame(self.root, bg=APP_BACKGROUND)
        header.pack(fill="x", padx=30, pady=(24, 18))
        tk.Label(
            header,
            text="MINIGAME TÊN MÓN QUÀ CỰC, CỰC KỲ Ý NGHĨA",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg=APP_BACKGROUND,
            anchor="center",
            justify="center",
        ).pack(fill="x")
        tk.Label(
            header,
            text="Chọn lần lượt các câu hỏi được đánh số từ 1 đến 12.",
            font=("Segoe UI", 11),
            fg="#e3f2fd",
            bg=APP_BACKGROUND,
            anchor="center",
            justify="center",
        ).pack(fill="x", pady=(4, 0))

        card = tk.Frame(
            self.root,
            bg=PAGE_BACKGROUND,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
        )
        card.pack(fill="both", expand=True, padx=30, pady=(0, 22))

        tk.Label(
            card,
            text="12 CÂU HỎI",
            font=("Segoe UI", 12, "bold"),
            fg="#202124",
            bg=PAGE_BACKGROUND,
            anchor="center",
            justify="center",
        ).pack(fill="x", padx=22, pady=(22, 5))
        tk.Label(
            card,
            text="Chọn số hoặc ô chữ tương ứng để mở câu hỏi.",
            font=("Segoe UI", 10),
            fg="#202124",
            bg=PAGE_BACKGROUND,
            anchor="center",
            justify="center",
        ).pack(fill="x", padx=22)

        board = tk.Frame(card, bg=PAGE_BACKGROUND)
        board.pack(pady=(24, 26))
        for column in range(len(ANSWER)):
            board.grid_columnconfigure(column, weight=1)

        for cell_index in range(len(ANSWER)):
            number_label = tk.Label(
                board,
                text=f"({cell_index + 1})",
                font=("Segoe UI", 12, "bold"),
                bg=PAGE_BACKGROUND,
                fg="#202124",
                cursor="hand2",
            )
            number_label.grid(
                row=0,
                column=cell_index,
                padx=6,
                pady=5,
                sticky="ew",
            )
            number_label.bind(
                "<Button-1>",
                lambda event, i=cell_index: self._on_question_label_click(
                    event, i
                ),
            )
            self.question_labels.append(number_label)

        for cell_index in range(len(ANSWER)):
            button = tk.Button(
                board,
                text=" ",
                width=3,
                height=2,
                font=("Consolas", 17, "bold"),
                relief="solid",
                bd=1,
                bg=BUTTON_BACKGROUND,
                fg="white",
                activebackground=BUTTON_BACKGROUND,
                activeforeground="white",
                highlightthickness=1,
                highlightbackground=BORDER_COLOR,
                highlightcolor=ACTIVE_BORDER_COLOR,
                anchor="center",
                cursor="hand2",
                command=lambda i=cell_index: self._show_question(i),
            )
            button.grid(
                row=1,
                column=cell_index,
                padx=6,
                pady=5,
                sticky="ew",
            )
            self.cell_buttons.append(button)

        question_panel = tk.Frame(
            card,
            bg=PAGE_BACKGROUND,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
        )
        question_panel.pack(fill="x", padx=22, pady=(0, 16))
        self.question_header = tk.Frame(question_panel, bg=PAGE_BACKGROUND)
        self.question_header.pack(fill="x", padx=18, pady=(18, 8))
        self.question_title_label = tk.Label(
            self.question_header,
            textvariable=self.question_title_var,
            font=("Segoe UI", 22, "bold"),
            fg="#202124",
            bg=PAGE_BACKGROUND,
            justify="center",
            wraplength=900,
        )
        self.question_title_label.pack(fill="x", padx=25, pady=20)
        self.question_header.bind(
            "<Configure>",
            lambda event: self.question_title_label.configure(
                wraplength=max(300, event.width - 60)
            ),
        )

        self.options_grid = tk.Frame(question_panel, bg=PAGE_BACKGROUND)
        self.options_grid.pack(fill="x", padx=20, pady=(8, 16))
        self.options_grid.grid_columnconfigure(0, weight=1, uniform="options")
        self.options_grid.grid_columnconfigure(1, weight=1, uniform="options")
        self.options_grid.grid_rowconfigure(0, weight=1, uniform="option_rows")
        self.options_grid.grid_rowconfigure(1, weight=1, uniform="option_rows")

        for choice_index in range(4):
            choice_button = tk.Frame(
                self.options_grid,
                bg=PAGE_BACKGROUND,
                highlightthickness=1,
                highlightbackground=BORDER_COLOR,
                cursor="hand2",
            )
            choice_button.grid(
                row=choice_index // 2,
                column=choice_index % 2,
                sticky="nsew",
                padx=8,
                pady=8,
            )
            choice_button.grid_columnconfigure(1, weight=1)
            choice_button.bind(
                "<Configure>",
                lambda event, i=choice_index: self._resize_choice_text(i, event.width),
            )
            choice_button.bind(
                "<Button-1>",
                lambda event, i=choice_index: self._on_choice_card_click(event, i),
            )

            badge = tk.Label(
                choice_button,
                text="ABCD"[choice_index],
                width=2,
                font=("Segoe UI", 14, "bold"),
                fg="#202124",
                bg=PAGE_BACKGROUND,
                padx=5,
                pady=7,
            )
            badge.grid(row=0, column=0, sticky="n", padx=(18, 14), pady=18)
            badge.bind(
                "<Button-1>",
                lambda event, i=choice_index: self._on_choice_card_click(event, i),
            )
            choice_text = tk.Label(
                choice_button,
                text="",
                font=("Segoe UI", 12, "bold"),
                fg="#202124",
                bg=PAGE_BACKGROUND,
                justify="left",
                anchor="w",
                wraplength=360,
                padx=6,
                pady=22,
            )
            choice_text.grid(row=0, column=1, sticky="nsew", padx=(0, 14))
            choice_text.bind(
                "<Button-1>",
                lambda event, i=choice_index: self._on_choice_card_click(event, i),
            )
            self.question_choices.append(choice_button)
            self.choice_badges.append(badge)
            self.choice_text_labels.append(choice_text)
            choice_button.grid_remove()

        self.feedback_label = tk.Label(
            question_panel,
            textvariable=self.feedback_var,
            font=("Segoe UI", 10, "bold"),
            fg="#b42318",
            bg=PAGE_BACKGROUND,
            anchor="center",
            justify="center",
        )
        status_bar = tk.Frame(self.root, bg=APP_BACKGROUND)
        status_bar.pack(fill="x", padx=30, pady=(0, 16))
        tk.Label(
            status_bar,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            fg="white",
            bg=APP_BACKGROUND,
            anchor="center",
            justify="center",
        ).pack(side="left", fill="x", expand=True)
        tk.Button(
            status_bar,
            text="Chơi lại",
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_BACKGROUND,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#ffffff",
            highlightcolor=ACTIVE_BORDER_COLOR,
            cursor="hand2",
            command=self._restart,
        ).pack(side="right")

    def _show_question(self, cell_index: int) -> None:
        if self.active_cell is not None:
            previous_cell = self.active_cell
            self.question_labels[previous_cell].configure(
                bg=PAGE_BACKGROUND,
                fg="#202124",
            )
            previous_background = (
                CORRECT_BACKGROUND
                if previous_cell in self.revealed
                else BUTTON_BACKGROUND
            )
            self.cell_buttons[previous_cell].configure(
                bg=previous_background,
                fg="white",
                activebackground=previous_background,
                highlightbackground=(
                    CORRECT_BACKGROUND
                    if previous_cell in self.revealed
                    else BORDER_COLOR
                ),
            )

        self.active_cell = cell_index
        question = QUESTIONS[cell_index]
        self.selected_choice.set(-1)
        self.feedback_var.set("")
        self.feedback_label.configure(fg="#b42318")
        self.question_title_var.set(f"Câu {cell_index + 1}: {question.clue}")
        if cell_index in self.revealed:
            self.status_var.set("Bạn đang xem lại câu hỏi đã trả lời.")
        self.question_labels[cell_index].configure(
            fg="#202124",
        )
        cell_background = (
            CORRECT_BACKGROUND if cell_index in self.revealed else BUTTON_BACKGROUND
        )
        self.cell_buttons[cell_index].configure(
            bg=cell_background,
            activebackground=cell_background,
            highlightbackground=ACTIVE_BORDER_COLOR,
        )

        for choice_index, choice_button in enumerate(self.question_choices):
            choice_button.configure(cursor="hand2")
            self.choice_text_labels[choice_index].configure(
                text=question.choices[choice_index]
            )
            self._style_choice(choice_index)
            choice_button.grid()
        self.feedback_label.pack(anchor="w", padx=14, pady=(4, 2))

    def _on_question_label_click(self, event: tk.Event, cell_index: int) -> None:
        if event.widget is self.question_labels[cell_index]:
            self._show_question(cell_index)

    def _resize_choice_text(self, choice_index: int, card_width: int) -> None:
        self.choice_text_labels[choice_index].configure(
            wraplength=max(180, card_width - 82)
        )

    def _style_choice(self, choice_index: int) -> None:
        if self.active_cell is None:
            return

        selected = self.selected_choice.get() == choice_index
        correct = (
            selected
            and choice_index == QUESTIONS[self.active_cell].correct_choice
            and self.feedback_var.get().startswith("✓")
        )
        wrong = selected and self.feedback_var.get().startswith("✗")

        background = BUTTON_BACKGROUND
        border = BORDER_COLOR
        badge_foreground = "white"
        foreground = "white"
        if selected:
            border = ACTIVE_BORDER_COLOR
        if wrong:
            background = WRONG_BACKGROUND
            border = WRONG_BACKGROUND
        elif correct:
            background = CORRECT_BACKGROUND
            border = CORRECT_BACKGROUND

        self.question_choices[choice_index].configure(
            bg=background,
            highlightbackground=border,
        )
        self.choice_badges[choice_index].configure(
            bg=background,
            fg=badge_foreground,
        )
        self.choice_text_labels[choice_index].configure(
            bg=background,
            fg=foreground,
        )

    def _select_choice(self, choice_index: int) -> None:
        if self.active_cell is None:
            return

        self.selected_choice.set(choice_index)
        self.feedback_var.set("")
        self.feedback_label.configure(fg="#b42318")
        for index in range(len(self.question_choices)):
            self._style_choice(index)
        self._check_answer()

    def _on_choice_card_click(self, event: tk.Event, choice_index: int) -> None:
        if event.widget in (
            self.question_choices[choice_index],
            self.choice_badges[choice_index],
            self.choice_text_labels[choice_index],
        ):
            self._select_choice(choice_index)

    def _show_completion_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Hoàn thành")
        dialog.configure(bg=PAGE_BACKGROUND)
        dialog.attributes("-fullscreen", True)
        dialog.bind("<Escape>", lambda _: dialog.destroy())
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        image_canvas = tk.Canvas(
            dialog,
            width=screen_width,
            height=screen_height,
            highlightthickness=0,
            bd=0,
        )
        image_canvas.pack(fill="both", expand=True)
        image_item = image_canvas.create_image(0, 0, anchor="nw")

        def display_image(image_path: str) -> None:
            try:
                with Image.open(image_path) as source:
                    fitted_image = ImageOps.fit(
                        source.convert("RGB"),
                        (screen_width, screen_height),
                        method=Image.Resampling.LANCZOS,
                    )
                image = ImageTk.PhotoImage(fitted_image, master=dialog)
            except (OSError, ValueError, tk.TclError) as exc:
                messagebox.showerror(
                    "Không thể mở ảnh",
                    f"Không thể tải ảnh đã chọn.\n\n{exc}",
                    parent=dialog,
                )
                return

            self.completion_image = image
            self.completion_image_path = image_path
            image_canvas.itemconfigure(image_item, image=image)

        def choose_image() -> None:
            image_path = filedialog.askopenfilename(
                parent=dialog,
                title="Chọn ảnh chúc mừng",
                filetypes=(
                    ("Ảnh", "*.png *.gif *.jpg *.jpeg *.webp *.bmp"),
                    ("Tất cả tệp", "*.*"),
                ),
            )
            if image_path:
                display_image(image_path)

        controls = tk.Frame(dialog, bg=PAGE_BACKGROUND)
        image_canvas.create_window(
            screen_width // 2,
            screen_height - 28,
            window=controls,
            anchor="center",
        )
        tk.Button(
            controls,
            text="Chọn ảnh",
            command=choose_image,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_BACKGROUND,
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=7,
        ).pack(side="left", padx=6)
        tk.Button(
            controls,
            text="Đóng",
            command=dialog.destroy,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=CORRECT_BACKGROUND,
            activebackground=CORRECT_BACKGROUND,
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=7,
        ).pack(side="left", padx=6)
        dialog.after_idle(
            lambda: display_image(self.completion_image_path)
        )

    def _check_answer(self) -> None:
        if self.active_cell is None:
            return

        question = QUESTIONS[self.active_cell]
        choice_index = self.selected_choice.get()
        if choice_index < 0:
            self.feedback_label.configure(fg="#b42318")
            self.feedback_var.set("Hãy chọn một đáp án trước khi kiểm tra.")
            return
        if choice_index != question.correct_choice:
            self.feedback_var.set("✗ Chưa chính xác. Hãy thử lại nhé!")
            self.feedback_label.configure(fg="#b42318")
            self._style_choice(choice_index)
            return

        cell_index = self.active_cell
        self.revealed.add(cell_index)
        self.feedback_var.set("✓ Chính xác!")
        self.feedback_label.configure(fg="#16803c")
        for index, choice_button in enumerate(self.question_choices):
            if index == choice_index:
                self._style_choice(index)
            choice_button.configure(cursor="arrow")
        self.question_labels[cell_index].configure(
            fg="#50e08b",
        )
        self.cell_buttons[cell_index].configure(
            text=ANSWER[cell_index],
            bg=CORRECT_BACKGROUND,
            fg="white",
            activebackground=CORRECT_BACKGROUND,
            activeforeground="white",
            highlightbackground=CORRECT_BACKGROUND,
        )
        self.active_cell = None
        self.status_var.set("Chính xác! Câu hỏi đã hoàn thành.")

        if len(self.revealed) == len(ANSWER) and not self.completion_announced:
            self.completion_announced = True
            self.status_var.set("Bạn đã trả lời đúng tất cả câu hỏi. Chúc mừng!")
            self._show_completion_dialog()

    def _restart(self) -> None:
        self.revealed.clear()
        self.completion_announced = False
        self.active_cell = None
        self.status_var.set("Chọn một số để trả lời câu hỏi!")
        for number_label in self.question_labels:
            number_label.configure(
                bg=PAGE_BACKGROUND,
                fg="#202124",
                cursor="hand2",
            )
        for button in self.cell_buttons:
            button.configure(
                text=" ",
                bg=BUTTON_BACKGROUND,
                fg="white",
                activebackground=BUTTON_BACKGROUND,
                activeforeground="white",
                highlightbackground=BORDER_COLOR,
                state=tk.NORMAL,
                cursor="hand2",
            )
        self.question_title_var.set("Chọn một số phía trên để xem câu hỏi.")
        self.selected_choice.set(-1)
        self.feedback_var.set("")
        self.feedback_label.configure(fg="#b42318")
        for index, choice_button in enumerate(self.question_choices):
            choice_button.configure(cursor="hand2")
            choice_button.grid_remove()
            choice_button.configure(
                bg=PAGE_BACKGROUND,
                highlightbackground=BORDER_COLOR,
            )
            self.choice_badges[index].configure(bg=BUTTON_BACKGROUND, fg="white")
            self.choice_text_labels[index].configure(
                bg=PAGE_BACKGROUND,
                fg="#202124",
            )
        self.feedback_label.pack_forget()


def main() -> None:
    validate_puzzle()
    root = tk.Tk()
    CrosswordGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
