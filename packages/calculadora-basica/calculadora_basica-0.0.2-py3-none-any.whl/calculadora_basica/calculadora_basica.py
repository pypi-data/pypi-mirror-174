# Importação de biblioteca tkinter
from tkinter import *
expression = ""

def input_number(number, equation):
	global expression
	expression = expression + str(number)
	equation.set(expression)
	
def clear_input_field(equation):
	global expression
	expression = ""
	equation.set("Informe uma expressão:")

def evaluate(equation):
	global expression
	try:
		result = str(eval(expression))
		equation.set(result)
	except:
		expression = ""

def main():
	window = Tk()
	window.title("Calculadora Básica")
	window.geometry("310x275")
	equation = StringVar()
	input_field = Entry(window, textvariable=equation)
	input_field.place(height=100)
	input_field.grid(columnspan=5)
	equation.set("Informe uma expressão:")
	btn_1 = Button(window, text="1", command=lambda: input_number(1, equation), width=5, font=("Arial", 14))
	btn_1.grid(row=2, column=1)
	btn_2 = Button(window, text="2", command=lambda: input_number(2, equation), width=5, font=("Arial", 14))
	btn_2.grid(row=2, column=2)
	btn_3 = Button(window, text="3", command=lambda: input_number(3, equation), width=5, font=("Arial", 14))
	btn_3.grid(row=2, column=3)
	btn_4 = Button(window, text="4", command=lambda: input_number(4, equation), width=5, font=("Arial", 14))
	btn_4.grid(row=3, column=1)
	btn_5 = Button(window, text="5", command=lambda: input_number(5, equation), width=5, font=("Arial", 14))
	btn_5.grid(row=3, column=2)
	btn_6 = Button(window, text="6", command=lambda: input_number(6, equation), width=5, font=("Arial", 14))
	btn_6.grid(row=3, column=3)
	btn_7 = Button(window, text="7", command=lambda: input_number(7, equation), width=5, font=("Arial", 14))
	btn_7.grid(row=4, column=1)
	btn_8 = Button(window, text="8", command=lambda: input_number(8, equation), width=5, font=("Arial", 14))
	btn_8.grid(row=4, column=2)
	btn_9 = Button(window, text="9", command=lambda: input_number(9, equation), width=5, font=("Arial", 14))
	btn_9.grid(row=4, column=3)
	btn_0 = Button(window, text="0", command=lambda: input_number(0, equation), width=5, font=("Arial", 14))
	btn_0.grid(row=5, column=2)
	btn_plus = Button(window, text="+", command=lambda: input_number('+', equation), width=5, font=("Arial", 14))
	btn_plus.grid(row=2, column=4)
	btn_minus = Button(window, text="-", command=lambda: input_number('-', equation), width=5, font=("Arial", 14))
	btn_minus.grid(row=3, column=4)
	btn_mul = Button(window, text="*", command=lambda: input_number('*', equation), width=5, font=("Arial", 14))
	btn_mul.grid(row=4, column=4)
	btn_div = Button(window, text="/", command=lambda: input_number('/', equation), width=5, font=("Arial", 14))
	btn_div.grid(row=5, column=4)
	btn_open = Button(window, text="(", command=lambda: input_number('(', equation), width=5, font=("Arial", 14))
	btn_open.grid(row=5, column=1)
	btn_close = Button(window, text=")", command=lambda: input_number(')', equation), width=5, font=("Arial", 14))
	btn_close.grid(row=5, column=3)
	btn_clear = Button(window, text="C", command=lambda: clear_input_field(equation), width=11, font=("Arial", 14))
	btn_clear.grid(row=6, column=1, columnspan=2)
	btn_equals = Button(window, text="=", command=lambda: evaluate(equation), width=11, font=("Arial", 14))
	btn_equals.grid(row=6, column=3, columnspan=2)
	window.mainloop()

if __name__ == '__main__':
	main()
