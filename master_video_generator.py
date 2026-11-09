import os
import subprocess

def run_command(cmd):
    print(f"Menjalankan: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise Exception("Perintah FFmpeg gagal.")
    print(result.stdout)

def generate_dummy_media(media_dir):
    os.makedirs(media_dir, exist_ok=True)
    foto1 = os.path.join(media_dir, "foto1.jpg")
    foto2 = os.path.join(media_dir, "foto2.png")
    video1 = os.path.join(media_dir, "video1.mp4")
    musik = os.path.join(media_dir, "musik.mp3")

    if not os.path.exists(foto1):
        print("Membuat foto dummy 1...")
        run_command(["ffmpeg", "-f", "lavfi", "-i", "color=c=red:s=1080x1920:d=1", "-frames:v", "1", foto1, "-y"])

    if not os.path.exists(foto2):
        print("Membuat foto dummy 2...")
        run_command(["ffmpeg", "-f", "lavfi", "-i", "color=c=blue:s=1080x1920:d=1", "-frames:v", "1", foto2, "-y"])

    if not os.path.exists(video1):
        print("Membuat video dummy 1...")
        run_command(["ffmpeg", "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30:duration=3", "-c:v", "libx264", "-pix_fmt", "yuv420p", video1, "-y"])

    if not os.path.exists(musik):
        print("Membuat musik dummy...")
        run_command(["ffmpeg", "-f", "lavfi", "-i", "sine=frequency=440:duration=5", "-c:a", "aac", "-b:a", "192k", musik, "-y"])

def main():
    media_dir = "media"
    generate_dummy_media(media_dir)
    temp_files = []
    print("=== MEMULAI PROSES MASTER VIDEO GENERATOR ===")
    
    foto1 = os.path.join(media_dir, "foto1.jpg")
    if os.path.exists(foto1):
        out_f1 = "temp_foto1.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto1, "-t", "3",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-y", out_f1
        ])
        temp_files.append(out_f1)

    vid1 = os.path.join(media_dir, "video1.mp4")
    if os.path.exists(vid1):
        out_v1 = "temp_video1.mp4"
        run_command([
            "ffmpeg", "-i", vid1,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-y", out_v1
        ])
        temp_files.append(out_v1)

    foto2 = os.path.join(media_dir, "foto2.png")
    if os.path.exists(foto2):
        out_f2 = "temp_foto2.mp4"
        run_command([
            "ffmpeg", "-loop", "1", "-i", foto2, "-t", "3",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-y", out_f2
        ])
        temp_files.append(out_f2)

    if not temp_files:
        print("Tidak ada file media yang ditemukan!")
        return

    list_txt = "concat_list.txt"
    with open(list_txt, "w") as f:
        for tf in temp_files:
            f.write(f"file '{tf}'\n")

    merged_vid = "temp_merged.mp4"
    run_command([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_txt,
        "-c", "copy", "-y", merged_vid
    ])

    music = os.path.join(media_dir, "musik.mp3")
    final_output = "Video_Profesional_Siap_Upload.mp4"
    
    if os.path.exists(music):
        print("Menambahkan musik latar belakang...")
        run_command([
            "ffmpeg", "-i", merged_vid, "-i", music,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-y", final_output
        ])
    else:
        os.rename(merged_vid, final_output)

    print(f"SUKSES! Video master profesional telah dibuat: {final_output}")

if __name__ == "__main__":
    main()
