import tkinter as tk
from tkinter import messagebox, font
from collections import deque





class ListNode:
    def _init_(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def _init_(self):
        self.head = None

    def insert_at_beginning(self, value):
        node = ListNode(value)
        node.next = self.head
        self.head = node

    def insert_at_end(self, value):
        node = ListNode(value)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete_value(self, value):
        cur = self.head
        prev = None
        while cur:
            if cur.data == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out


class Stack:
    def _init_(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if not self._data:
            return None
        return self._data.pop()

    def peek(self):
        if not self._data:
            return None
        return self._data[-1]

    def to_list(self):
        # Return bottom->top
        return list(self._data)


class Queue:
    def _init_(self):
        self._data = deque()

    def enqueue(self, value):
        self._data.append(value)

    def dequeue(self):
        if not self._data:
            return None
        return self._data.popleft()

    def front(self):
        if not self._data:
            return None
        return self._data[0]

    def to_list(self):
        return list(self._data)





class App(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Data Structure Visualizer")
        self.geometry("800x500")
        self.resizable(False, False)

        # Container for pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, LinkedListPage, StackPage, QueuePage):
            page_name = F._name_
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller

        title_font = font.Font(size=20, weight="bold")
        tk.Label(self, text="Data Structure Visualizer", font=title_font).pack(pady=30)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Linked List", width=20,
                  command=lambda: controller.show_frame("LinkedListPage")).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Stack", width=20,
                  command=lambda: controller.show_frame("StackPage")).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Queue", width=20,
                  command=lambda: controller.show_frame("QueuePage")).grid(row=2, column=0, padx=10, pady=5)


class LinkedListPage(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller

        self.linked_list = LinkedList()

        header = tk.Frame(self)
        header.pack(fill="x", pady=6)
        tk.Label(header, text="Singly Linked List", font=font.Font(size=14, weight="bold")).pack()

        control = tk.Frame(self)
        control.pack(fill="x", pady=4)

        tk.Label(control, text="Value:").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(control)
        self.entry.grid(row=0, column=1, padx=5)

        tk.Button(control, text="Insert Head", command=self.insert_head).grid(row=0, column=2, padx=4)
        tk.Button(control, text="Insert Tail", command=self.insert_tail).grid(row=0, column=3, padx=4)
        tk.Button(control, text="Delete", command=self.delete_value).grid(row=0, column=4, padx=4)
        tk.Button(control, text="Clear", command=self.clear).grid(row=0, column=5, padx=4)
        tk.Button(control, text="Back", command=lambda: controller.show_frame("HomePage")).grid(row=0, column=6, padx=4)

        # Canvas for drawing
        self.canvas = tk.Canvas(self, width=760, height=320, bg="white")
        self.canvas.pack(pady=8)

        # Drawing constants
        self.start_x = 50
        self.start_y = 100
        self.node_w = 60
        self.node_h = 40
        self.gap = 30

        # For temporary highlight animation
        self._highlight_idx = None

        self.draw()

    def _get_input(self):
        value = self.entry.get().strip()
        if value == "":
            messagebox.showwarning("Input required", "Please enter a value.")
            return None
        return value

    def insert_head(self):
        v = self._get_input()
        if v is None:
            return
        self.linked_list.insert_at_beginning(v)
        # highlight index 0
        self._highlight_idx = 0
        self.draw()
        # schedule to clear highlight
        self.after(400, lambda: (setattr(self, "_highlight_idx", None), self.draw()))

    def insert_tail(self):
        v = self._get_input()
        if v is None:
            return
        self.linked_list.insert_at_end(v)
        # highlight last index
        self._highlight_idx = len(self.linked_list.to_list()) - 1
        self.draw()
        self.after(400, lambda: (setattr(self, "_highlight_idx", None), self.draw()))

    def delete_value(self):
        v = self._get_input()
        if v is None:
            return
        ok = self.linked_list.delete_value(v)
        if not ok:
            messagebox.showinfo("Not found", f"Value '{v}' not found in list.")
        self.draw()

    def clear(self):
        self.linked_list = LinkedList()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        vals = self.linked_list.to_list()
        x = self.start_x
        y = self.start_y
        for i, val in enumerate(vals):
            fill = "#e6f7ff" if i == self._highlight_idx else "#ffffff"
            outline = "#007acc" if i == self._highlight_idx else "#000000"
            # rectangle
            self.canvas.create_rectangle(x, y, x + self.node_w, y + self.node_h, fill=fill, outline=outline, width=2)
            # text
            self.canvas.create_text(x + self.node_w / 2, y + self.node_h / 2, text=str(val))
            # arrow to next
            if i < len(vals) - 1:
                x1 = x + self.node_w
                y1 = y + self.node_h / 2
                x2 = x + self.node_w + self.gap
                y2 = y + self.node_h / 2
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)
            x += self.node_w + self.gap


class StackPage(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        self.stack = Stack()

        header = tk.Frame(self)
        header.pack(fill="x", pady=6)
        tk.Label(header, text="Stack", font=font.Font(size=14, weight="bold")).pack()

        control = tk.Frame(self)
        control.pack(fill="x", pady=4)

        tk.Label(control, text="Value:").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(control)
        self.entry.grid(row=0, column=1, padx=5)

        tk.Button(control, text="Push", command=self.push).grid(row=0, column=2, padx=4)
        tk.Button(control, text="Pop", command=self.pop).grid(row=0, column=3, padx=4)
        tk.Button(control, text="Peek", command=self.peek).grid(row=0, column=4, padx=4)
        tk.Button(control, text="Clear", command=self.clear).grid(row=0, column=5, padx=4)
        tk.Button(control, text="Back", command=lambda: controller.show_frame("HomePage")).grid(row=0, column=6, padx=4)

        self.canvas = tk.Canvas(self, width=760, height=320, bg="white")
        self.canvas.pack(pady=8)

        # drawing metrics
        self.box_w = 120
        self.box_h = 40
        self.gap = 10

        self.draw()

    def _get_input(self):
        value = self.entry.get().strip()
        if value == "":
            messagebox.showwarning("Input required", "Please enter a value.")
            return None
        return value

    def push(self):
        v = self._get_input()
        if v is None:
            return
        self.stack.push(v)
        self.draw()

    def pop(self):
        val = self.stack.pop()
        if val is None:
            messagebox.showinfo("Empty", "Stack is empty.")
        else:
            messagebox.showinfo("Popped", f"Popped value: {val}")
        self.draw()

    def peek(self):
        val = self.stack.peek()
        if val is None:
            messagebox.showinfo("Empty", "Stack is empty.")
        else:
            messagebox.showinfo("Top", f"Top value: {val}")

    def clear(self):
        self.stack = Stack()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        vals = self.stack.to_list()  # bottom->top
        # draw from bottom up
        canvas_h = int(self.canvas['height'])
        x_center = 380
        y_bottom = canvas_h - 20
        for i, val in enumerate(vals):
            # index from bottom: i -> y
            y = y_bottom - (len(vals) - 1 - i) * (self.box_h + self.gap)
            x1 = x_center - self.box_w / 2
            x2 = x_center + self.box_w / 2
            self.canvas.create_rectangle(x1, y - self.box_h, x2, y, fill="#fff2e6", outline="#cc7a00", width=2)
            self.canvas.create_text((x1 + x2) / 2, y - self.box_h / 2, text=str(val))


class QueuePage(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        self.queue = Queue()

        header = tk.Frame(self)
        header.pack(fill="x", pady=6)
        tk.Label(header, text="Queue", font=font.Font(size=14, weight="bold")).pack()

        control = tk.Frame(self)
        control.pack(fill="x", pady=4)

        tk.Label(control, text="Value:").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(control)
        self.entry.grid(row=0, column=1, padx=5)

        tk.Button(control, text="Enqueue", command=self.enqueue).grid(row=0, column=2, padx=4)
        tk.Button(control, text="Dequeue", command=self.dequeue).grid(row=0, column=3, padx=4)
        tk.Button(control, text="Front", command=self.front).grid(row=0, column=4, padx=4)
        tk.Button(control, text="Clear", command=self.clear).grid(row=0, column=5, padx=4)
        tk.Button(control, text="Back", command=lambda: controller.show_frame("HomePage")).grid(row=0, column=6, padx=4)

        self.canvas = tk.Canvas(self, width=760, height=320, bg="white")
        self.canvas.pack(pady=8)

        # drawing constants
        self.start_x = 50
        self.start_y = 140
        self.node_w = 60
        self.node_h = 40
        self.gap = 30

        self.draw()

    def _get_input(self):
        v = self.entry.get().strip()
        if v == "":
            messagebox.showwarning("Input required", "Please enter a value.")
            return None
        return v

    def enqueue(self):
        v = self._get_input()
        if v is None:
            return
        self.queue.enqueue(v)
        self.draw()

    def dequeue(self):
        val = self.queue.dequeue()
        if val is None:
            messagebox.showinfo("Empty", "Queue is empty.")
        else:
            messagebox.showinfo("Dequeued", f"Dequeued value: {val}")
        self.draw()

    def front(self):
        val = self.queue.front()
        if val is None:
            messagebox.showinfo("Empty", "Queue is empty.")
        else:
            messagebox.showinfo("Front", f"Front value: {val}")

    def clear(self):
        self.queue = Queue()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        vals = self.queue.to_list()
        x = self.start_x
        y = self.start_y
        for i, val in enumerate(vals):
            self.canvas.create_rectangle(x, y, x + self.node_w, y + self.node_h, fill="#e6ffe6", outline="#009900", width=2)
            self.canvas.create_text(x + self.node_w / 2, y + self.node_h / 2, text=str(val))
            # arrow to next
            if i < len(vals) - 1:
                x1 = x + self.node_w
                y1 = y + self.node_h / 2
                x2 = x + self.node_w + self.gap
                y2 = y + self.node_h / 2
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)
            x += self.node_w + self.gap

        # labels for front and rear
        if vals:
            # front label above first
            fx = self.start_x + self.node_w / 2
            fy = y - 20
            self.canvas.create_text(fx, fy, text="Front", fill="#333333", font=(None, 10, 'bold'))
            # rear label above last
            rx = self.start_x + (self.node_w + self.gap) * (len(vals) - 1) + self.node_w / 2
            ry = y - 20
            self.canvas.create_text(rx, ry, text="Rear", fill="#333333", font=(None, 10, 'bold'))


if _name_ == "_main_":
    app = App()
    app.mainloop()
