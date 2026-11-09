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
    
    print("=== MEMULAI PROSES VIDEO DINAMIS DARI 1 FOTO (KEN BURNS EFFECT) ===")
    
    foto1 = os.path.join(media_dir, "foto1.jpg")
    if os.path.exists(foto1):
        # 1. Bagian Pertama: Efek Zoom-In Perlahan (Mendekat)
        out_f1 = "temp_foto_zoom_in.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto1, "-t", "3",
            "-vf", "scale=2000:2000,zoompan=z='min(zoom+0.0015,1.5)':d=90:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", "-y", out_f1
        ])
        temp_files.append(out_f1)

        # 2. Bagian Kedua: Efek Zoom-Out Perlahan (Menjauh / Berbeda Gaya)
        out_f2 = "temp_foto_zoom_out.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto1, "-t", "3",
            "-vf", "scale=2000:2000,zoompan=z='if(lte(zoom,1.0),1.5,max(zoom-0.0015,1.0))':d=90:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", "-y", out_f2
        ])
        temp_files.append(out_f2)

    if not temp_files:
        print("Error: File foto1.jpg tidak ditemukan di folder media/!")
        return

    # 3. Gabungkan gaya-gaya tersebut menjadi satu kesatuan video
    list_txt = "concat_list.txt"
    with open(list_txt, "w") as f:
        for tf in temp_files:
            f.write(f"file '{tf}'\n")

    merged_vid = "temp_merged.mp4"
    run_command([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_txt,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-y", merged_vid
    ])

    # 4. Tambahkan Audio (Voiceover atau Musik) jika ada
    voiceover = os.path.join(media_dir, "voiceover.mp3")
    music = os.path.join(media_dir, "musik.mp3")
    final_output = "Video_Profesional_Siap_Upload.mp4"
    
    if os.path.exists(voiceover):
        print("Menambahkan suara asli (voiceover)...")
        run_command([
            "ffmpeg", "-i", merged_vid, "-i", voiceover,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-y", final_output
        ])
    elif os.path.exists(music):
        print("Menambahkan musik latar...")
        run_command([
            "ffmpeg", "-i", merged_vid, "-i", music,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-y", final_output
        ])
    else:
        os.rename(merged_vid, final_output)

    print(f"SUKSES! 1 Foto berhasil diubah menjadi video berbagai gaya: {final_output}")

if __name__ == "__main__":
    main()
