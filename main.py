from PersianCaptchaSolver import CaptchaSolver

captcha_path = "captcha.jpg"
extracted_text , result = CaptchaSolver.Solve(captcha_path)
print(extracted_text) # 8+4
print(result) # 12