import lzma
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

KERNEL = platform.system().lower()
ARCHITECTURE = platform.machine().lower().replace("amd64", "x86_64")
SYSTEM = f"{KERNEL}.{ARCHITECTURE}"


def check_executable(*names):
    for name in names:
        if not shutil.which(name):
            raise RuntimeError(f"executable not found: {name}")


def make_tar_archive(in_path, out_path):
    with tarfile.open(out_path, "w:xz") as tar:
        tar.add(in_path, arcname=os.path.basename(in_path))


def decompress_tar_archive(in_path, in_base_path, out_path):
    with tarfile.open(in_path, "r") as in_file:
        with tempfile.TemporaryDirectory() as tmp_dir:
            in_file.extractall(tmp_dir)
            shutil.move(os.path.join(tmp_dir, in_base_path), out_path)


os.chdir(os.path.dirname(__file__))

if not os.path.isdir("libbigwig"):
    os.mkdir("libbigwig")
libbigwig_dir = os.path.join("libbigwig", SYSTEM)
if os.path.isdir(libbigwig_dir):
    shutil.rmtree(libbigwig_dir)
with urllib.request.urlopen("https://github.com/dpryan79/libBigWig/archive/refs/tags/0.4.7.tar.gz") as in_file:
    with open("libbigwig.tmp", "wb") as out_file:
        out_file.write(in_file.read())
decompress_tar_archive("libbigwig.tmp", "libBigWig-0.4.7", libbigwig_dir)
os.remove("libbigwig.tmp")
check_executable("gcc", "ar")
compile_files = ["bwRead", "bwStats", "bwValues", "bwWrite", "io"]
for file in compile_files:
    subprocess.run([
        "gcc", os.path.join(libbigwig_dir, f"{file}.c"),
        "-c", "-g", "-Wall", "-O3", "-Wsign-compare", "-lm", "-lz", "-DNOCURL",
        "-o", os.path.join(libbigwig_dir, f"{file}.o")],
        check=True)
subprocess.run([
    "ar", "rcs", os.path.join(libbigwig_dir, "libBigWig.a"),
    *(os.path.join(libbigwig_dir, f"{file}.o") for file in compile_files)],
    check=True)
os.mkdir(os.path.join(libbigwig_dir, "bin"))
for file in ["bigwig_reader", "bigbed_reader", "bbi_header_reader"]:
    subprocess.run([
        "gcc", os.path.join("..", "signal_c_lib", f"{file}.c"),
        os.path.join(libbigwig_dir, "libBigWig.a"),
        "-I", libbigwig_dir, "-lm", "-lz", "-DNOCURL", "-O3",
        "-o", os.path.join(libbigwig_dir, "bin", f"{file}.exe")],
        check=True)
make_tar_archive(libbigwig_dir, os.path.join("libbigwig", f"{SYSTEM}.tar.xz"))
shutil.rmtree(libbigwig_dir)
