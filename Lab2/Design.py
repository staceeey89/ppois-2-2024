from PyQt5.QtCore import Qt


class Design:
    def design_button(button, x_pos=0, y_pos=0, text="", width=153, height=39, br_radius=15, bg_color="#572774",
                      br_color="white", fn_size=15):
        button.setText(text)
        button.setGeometry(x_pos, y_pos, width, height)
        button.setStyleSheet(f"background-color: {bg_color}; border: 2px solid {br_color}; "
                             f"color: white; border-radius: {br_radius}px; font-size: {fn_size}px;")
        button.setCursor(Qt.PointingHandCursor)

    def design_text(des_text, x_pos=0, y_pos=0, text="", font_size=15, width=102, height=30, color="white"):
        des_text.setText(text)
        des_text.adjustSize()
        des_text.setGeometry(x_pos, y_pos, width, height)
        des_text.setStyleSheet(f"color: {color}; font-size: {font_size}px;")

    def design_home_button(button, x_pos=0, y_pos=0):
        button.setGeometry(x_pos, y_pos, 37, 37)
        button.setStyleSheet("background-color: #572774; border: 2px solid white;"
                             " border-radius: 18px; background-image: url(img/home.png)")
        button.setCursor(Qt.PointingHandCursor)

    def design_input_field(input_field, x_pos=0, y_pos=0, width=296, height=39, br_radius=15, bg_color="#060946",
                           br_color="white", fn_size=15):
        input_field.setGeometry(x_pos, y_pos, width, height)
        input_field.setStyleSheet(f"background-color: {bg_color}; border: 2px solid {br_color}; "
                                  f"color: white; border-radius: {br_radius}px; font-size: {fn_size}px")

    def design_combo_box(combo_box, x_pos=0, y_pos=0, width=45, height=45,
                         bg_color="#572774", br_color="white", color="white"):
        combo_box.setGeometry(x_pos, y_pos, width, height)
        combo_box.setStyleSheet(f"background-color: {bg_color}; border: 2px solid {br_color}; color: {color}")
        combo_box.setCursor(Qt.PointingHandCursor)
