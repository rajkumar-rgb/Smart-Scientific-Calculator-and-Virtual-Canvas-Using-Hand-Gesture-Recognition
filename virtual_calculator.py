import cv2
import math
import time
import mediapipe as mp

# ================= BUTTON =================
class Button:
    def __init__(self, x, y, w, h, v):
        self.x, self.y, self.w, self.h = int(x), int(y), int(w), int(h)
        self.v = v

    def draw(self, img):
        cv2.rectangle(img, (self.x, self.y),
                      (self.x + self.w, self.y + self.h),
                      (30, 30, 30), -1)
        cv2.rectangle(img, (self.x, self.y),
                      (self.x + self.w, self.y + self.h),
                      (220, 220, 220), 1)

        font_scale = (self.h * 0.38) / 30
        (tw, th), _ = cv2.getTextSize(self.v,
                                     cv2.FONT_HERSHEY_SIMPLEX,
                                     font_scale, 1)
        cv2.putText(img, self.v,
                    (self.x + (self.w - tw) // 2,
                     self.y + (self.h + th) // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (255, 255, 255), 1, cv2.LINE_AA)

    def hit(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h


# ================= KEYS =================
keys = [
    ["Deg", "Rad", "x!", "(", ")", "%", "AC"],
    ["Back", "sin", "ln", "7", "8", "9", "/"],
    ["pi", "cos", "log", "4", "5", "6", "*"],
    ["e", "tan", "sqrt", "1", "2", "3", "-"],
    ["Ans", "EXP", "pow", "0", ".", "=", "+"]
]


# ================= CALCULATOR =================
def run_calculator(cap, hands):
    mp_draw = mp.solutions.drawing_utils
    
    # equation stores tuples: (visual_text, code_text)
    # Example: [("sin(", "math.sin(math.radians("), ("90", "90"), (")", "))")]
    equation = [] 
    ans = ""
    last_click = 0
    use_degree = True

    cv2.namedWindow("Calculator", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Calculator",
                          cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    ret, img = cap.read()
    h, w, _ = img.shape

    panel_w = int(w * 0.70)
    panel_x = (w - panel_w) // 2

    disp_h = 90
    disp_x = panel_x + 40
    disp_w = panel_w - 80

    rows, cols = 5, 7
    grid_top = disp_h + 120
    grid_w = panel_w - 80
    grid_h = h - grid_top - 90

    bh = (grid_h / rows) * 1.10
    bw = (grid_w / cols) * 1.05

    buttons = []
    for r in range(rows):
        for c in range(cols):
            buttons.append(
                Button(panel_x + 40 + c * bw,
                       grid_top + r * bh,
                       bw - 14, bh - 14,
                       keys[r][c])
            )

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        # ---------- DISPLAY BACKGROUND ----------
        cv2.rectangle(img, (disp_x, 40),
                      (disp_x + disp_w, 40 + disp_h),
                      (0, 0, 0), -1)
        cv2.rectangle(img, (disp_x, 40),
                      (disp_x + disp_w, 40 + disp_h),
                      (0, 255, 255), 3)

        # Build the Visual String from the equation list
        display_text = "".join([x[0] for x in equation])

        # ✅ AUTO-SCROLL DISPLAY
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 2
        padding = 20
        max_width = disp_w - 2 * padding

        # Scroll text if too long
        scroll_text = display_text
        while True:
            (tw, _), _ = cv2.getTextSize(scroll_text,
                                         font, font_scale, thickness)
            if tw <= max_width or len(scroll_text) == 0:
                break
            scroll_text = scroll_text[1:]

        cv2.putText(img, scroll_text,
                    (disp_x + padding, 100),
                    font, font_scale,
                    (0, 255, 255), thickness)

        for b in buttons:
            b.draw(img)
            # Highlight active mode buttons
            if (b.v == "Deg" and use_degree) or (b.v == "Rad" and not use_degree):
                cv2.rectangle(img, (b.x, b.y), (b.x + b.w, b.y + b.h), (0, 255, 0), 2)

        # ---------- HAND INPUT ----------
        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, lm,
                                   mp.solutions.hands.HAND_CONNECTIONS)

            x1 = int(lm.landmark[4].x * w)
            y1 = int(lm.landmark[4].y * h)
            x2 = int(lm.landmark[8].x * w)
            y2 = int(lm.landmark[8].y * h)

            if math.hypot(x2 - x1, y2 - y1) < 40 and time.time() - last_click > 0.6:
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                for b in buttons:
                    if b.hit(cx, cy):
                        v = b.v
                        
                        if v == "AC":
                            equation.clear()
                        elif v == "Back":
                            if equation:
                                equation.pop()
                        
                        elif v == "=":
                            # 1. Construct the Python code string
                            code_expr = "".join([x[1] for x in equation])
                            
                            # 2. Auto-close brackets based on open count in code string
                            open_bk = code_expr.count("(")
                            close_bk = code_expr.count(")")
                            if open_bk > close_bk:
                                code_expr += ")" * (open_bk - close_bk)
                            
                            try:
                                res = eval(code_expr)
                                # Rounding logic to fix tan(45) = 0.99999
                                if isinstance(res, float):
                                    res = round(res, 8)
                                    if res.is_integer():
                                        res = int(res)
                                ans = str(res)
                                # Reset equation to the answer
                                equation = [(ans, ans)]
                            except:
                                equation = [("Error", "Error")]
                        
                        elif v == "Ans":
                            equation.append((ans, ans))
                        elif v == "Deg":
                            use_degree = True
                        elif v == "Rad":
                            use_degree = False
                        
                        # === TRIGONOMETRY & MAPPING LOGIC ===
                        elif v == "sin":
                            if use_degree:
                                equation.append(("sin(", "math.sin(math.radians("))
                            else:
                                equation.append(("sin(", "math.sin("))
                        elif v == "cos":
                            if use_degree:
                                equation.append(("cos(", "math.cos(math.radians("))
                            else:
                                equation.append(("cos(", "math.cos("))
                        elif v == "tan":
                            if use_degree:
                                equation.append(("tan(", "math.tan(math.radians("))
                            else:
                                equation.append(("tan(", "math.tan("))
                        
                        elif v == "ln":
                            equation.append(("ln(", "math.log("))
                        elif v == "log":
                            equation.append(("log(", "math.log10("))
                        elif v == "sqrt":
                            equation.append(("sqrt(", "math.sqrt("))
                        elif v == "pi":
                            equation.append(("π", "math.pi"))
                        elif v == "e":
                            equation.append(("e", "math.e"))
                        elif v == "pow":
                            equation.append(("^", "**"))
                        elif v == "EXP":
                            equation.append(("E", "*10**"))
                        elif v == "%":
                            equation.append(("%", "/100"))
                            
                        elif v == "x!":
                            # Special case: Evaluate current, apply factorial, reset
                            try:
                                curr_code = "".join([x[1] for x in equation])
                                val = eval(curr_code)
                                res = math.factorial(int(val))
                                equation = [(str(res), str(res))]
                            except:
                                equation = [("Error", "Error")]
                                
                        else:
                            # Numbers and basic operators (1, 2, +, -)
                            equation.append((v, v))
                        
                        last_click = time.time()

        cv2.imshow("Calculator", img)

        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyWindow("Calculator")
            return