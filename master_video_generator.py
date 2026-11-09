import os
import subprocess

def run_command(cmd):
    print(f"Menjalankan: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise Exception("Perintah FFmpeg gagal.")
    print(result.stdout)

def main():
    media_dir = "media"
    temp_files = []
    
    print("=== MEMULAI PROSES MASTER VIDEO PROFESIONAL (ANTI-BAN) ===")
    
    # 1. Proses Foto 1 (Pastikan foto asli, bukan hasil screenshot ber-watermark)
    foto1 = os.path.join(media_dir, "foto1.jpg")
    if os.path.exists(foto1):
        out_f1 = "temp_foto1.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto1, "-t", "3",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-an", "-y", out_f1
        ])
        temp_files.append(out_f1)

    # 2. Proses Video Sumber Utama (video1.mp4 - Dijamin bersih dari watermark luar)
    vid1 = os.path.join(media_dir, "video1.mp4")
    if os.path.exists(vid1):
        out_v1 = "temp_video1.mp4"
        run_command([
            "ffmpeg", "-i", vid1,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-an", "-y", out_v1
        ])
        temp_files.append(out_v1)

    # 3. Proses Foto 2 (Opsional untuk variasi konten agar tidak monoton/dianggap spam)
    foto2 = os.path.join(media_dir, "foto2.jpg")
    if os.path.exists(foto2):
        out_f2 = "temp_foto2.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto2, "-t", "3",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-an", "-y", out_f2
        ])
        temp_files.append(out_f2)

    if not temp_files:
        print("Error: Tidak ada file media yang ditemukan di folder media/!")
        return

    # 4. Buat daftar urutan file untuk digabung
    list_txt = "concat_list.txt"
    with open(list_txt, "w") as f:
        for tf in temp_files:
            f.write(f"file '{tf}'\n")

    # 5. Gabungkan semua klip video secara bersih
    merged_vid = "temp_merged.mp4"
    run_command([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_txt,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-y", merged_vid
    ])

    # 6. Pengaturan Musik Latar Belakang (Opsional)
    # REKOMENDASI ANTI-BAN: Kosongkan/hapus file musik.mp3 dari folder media jika ingin 
    # memakai musik tren langsung dari aplikasi TikTok/Shopee agar terhindar dari copyright.
    music = os.path.join(media_dir, "musik.mp3")
    final_output = "Video_Profesional_Siap_Upload.mp4"
    
    if os.path.exists(music):
        print("Menambahkan musik latar...")
        run_command([
            "ffmpeg", "-i", merged_vid, "-i", music,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-y", final_output
        ])
    else:
        print("Tanpa musik latar internal. Video aman untuk diberi musik tren langsung di aplikasi.")
        os.rename(merged_vid, final_output)

    print(f"SUKSES! Master video profesional siap di-upload: {final_output}")

if __name__ == "__main__":
    main()
