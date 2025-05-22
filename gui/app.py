# gui/app.py
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox  
from md2pt_jp.converter import convert_markdown_to_plaintext  # ← 追加

def main():
    root = tk.Tk()
    root.title("md2pt_jp GUI")
    root.geometry("800x600")

    input_text = ""
    output_box = None

    def open_file():
        nonlocal input_text
        filepath = filedialog.askopenfilename(
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                input_text = f.read()
                input_box.delete("1.0", tk.END)
                input_box.insert(tk.END, input_text)

    def convert_text():
        # input_text に依存せず、常に input_box の中身を読むように変更
        raw_input = input_box.get("1.0", tk.END).strip()
        if raw_input:
            status_var.set("変換中...")
            root.update_idletasks()
            converted = convert_markdown_to_plaintext(raw_input)
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, converted)
            status_var.set("変換完了！")
        else:
            status_var.set("入力が空です")

    def save_output():
        content = output_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "保存する内容がありません。")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("保存完了", f"保存しました：\n{filepath}")
            status_var.set("保存完了")

    def save_to_clipboard():
        content = output_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "クリップボードに保存する内容がありません。")
            return

        root.clipboard_clear()
        root.clipboard_append(content)
        root.update_idletasks()
        status_var.set("クリップボードに保存しました")

    # UI要素の配置
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    open_button = tk.Button(top_frame, text="Markdownファイルを選択", command=open_file)
    open_button.pack(side=tk.LEFT, padx=5)

    convert_button = tk.Button(top_frame, text="変換", command=convert_text)
    convert_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(top_frame, text="変換結果を保存", command=save_output)
    save_button.pack(side=tk.LEFT, padx=5)

    clipboard_button = tk.Button(top_frame, text="クリップボードに保存", command=save_to_clipboard)
    clipboard_button.pack(side=tk.LEFT, padx=5)
    
    input_label = tk.Label(root, text="Markdown内容")
    input_label.pack()
    input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
    input_box.pack(fill="both", expand=True, padx=10, pady=5)
    
    # === ダイアグラム描画用 Canvas ===
    diagram_canvas = tk.Canvas(root, width=600, height=120, bg="#f5f5f5")
    diagram_canvas.pack(pady=10)

    # 図形の描画（初期状態）
    diagram_canvas.create_rectangle(30, 30, 150, 80, fill="#e1f5fe", outline="black")
    diagram_canvas.create_text(90, 55, text="Markdown", font=("Arial", 10))

    diagram_canvas.create_rectangle(230, 30, 350, 80, fill="#fff9c4", outline="black")
    diagram_canvas.create_text(290, 55, text="変換処理", font=("Arial", 10))

    diagram_canvas.create_rectangle(430, 30, 550, 80, fill="#c8e6c9", outline="black")
    diagram_canvas.create_text(490, 55, text="Plaintext", font=("Arial", 10))

    # 矢印線
    diagram_canvas.create_line(150, 55, 230, 55, arrow=tk.LAST, width=2)
    diagram_canvas.create_line(350, 55, 430, 55, arrow=tk.LAST, width=2)
    
    output_label = tk.Label(root, text="変換結果（プレーンテキスト）")
    output_label.pack()
    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
    output_box.pack(fill="both", expand=True, padx=10, pady=5)

    # === ステータスバー ===
    status_var = tk.StringVar()
    status_var.set("準備完了")

    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()
