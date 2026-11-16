# TrueWhys Kaggle GPU render kernel for Style R Shorts (Blender 5.0.1 + MPFB 2.0.18, CC0 output).
# Dataset (flat): scene.py, shots.json, sr_*.py, camera.py, mpfb.zip, job.json {"w":1080,"h":1920,"samples":64,"step":1,"mblur":true,"shots":null}
import subprocess, glob, os, json, time, shutil
t0 = time.time()
cfgp = glob.glob('/kaggle/input/**/job.json', recursive=True)[0]
D = os.path.dirname(cfgp); job = json.load(open(cfgp))
print("dataset dir", D, job, flush=True)
subprocess.run("nvidia-smi", shell=True)
if not os.path.exists('/tmp/blender/blender'):
    subprocess.run('wget -q https://download.blender.org/release/Blender5.0/blender-5.0.1-linux-x64.tar.xz -O /tmp/b.tar.xz && '
                   'mkdir -p /tmp/blender && tar -xf /tmp/b.tar.xz -C /tmp/blender --strip-components=1', shell=True, check=True)
subprocess.run('apt-get -qq install -y libxkbcommon0 libsm6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 >/dev/null 2>&1', shell=True)
B = '/tmp/blender/blender'
W = '/tmp/work'; shutil.copytree(D, W, dirs_exist_ok=True)          # writable copy, scripts side by side
# MPFB: Kaggle unpacks .zip files inside datasets, so the package is uploaded as mpfb_zip.bin (copied back to .zip here);
# if a .zip was unpacked anyway, copy the folder holding blender_manifest.toml straight into the user extensions repo.
EXT = os.path.expanduser('~/.config/blender/5.0/extensions/user_default/mpfb')
binf = glob.glob(f'{D}/**/mpfb_zip.bin', recursive=True) + glob.glob(f'{D}/**/mpfb.zip', recursive=True)
if binf:
    shutil.copy(binf[0], '/tmp/mpfb.zip')
    inst = ('import bpy,addon_utils;bpy.ops.extensions.package_install_files(filepath="/tmp/mpfb.zip", repo="user_default", enable_on_install=True);'
            'print("MPFB", addon_utils.enable("bl_ext.user_default.mpfb", default_set=True) is not None)')
    print(subprocess.run([B, '-b', '--python-expr', inst], capture_output=True, text=True).stdout[-600:], flush=True)
if not os.path.exists(EXT):
    man = [m for m in glob.glob('/kaggle/input/**/blender_manifest.toml', recursive=True) if 'mpfb' in open(m).read().lower()]
    if man:
        shutil.copytree(os.path.dirname(man[0]), EXT, dirs_exist_ok=True)
        print("MPFB copied from", os.path.dirname(man[0]), flush=True)
chk = subprocess.run([B, '-b', '--python-expr', 'import addon_utils;print("MPFB_OK", addon_utils.enable("bl_ext.user_default.mpfb", default_set=True) is not None)'],
                     capture_output=True, text=True).stdout
print([l for l in chk.splitlines() if 'MPFB_OK' in l], flush=True)
out = '/kaggle/working/frames'; os.makedirs(out, exist_ok=True)
ngpu = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 1)
procs = []
for i in range(ngpu):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(i), TW_DEADLINE=str(t0 + job.get("deadline", 37800)))
    cmd = [B, '-b', '--python', f'{W}/scene.py', '--', f'{W}/shots.json', out, '--w', str(job['w']), '--h', str(job['h']),
           '--samples', str(job['samples']), '--step', str(job.get('step', 1)), '--gpu', '--part', f'{i}/{ngpu}', '--jpg'] + (['--mblur'] if job.get('mblur') else [])
    if job.get('shots'):
        cmd += ['--shots', job['shots']]
    procs.append(subprocess.Popen(cmd, env=env, cwd=W, stdout=open(f'/kaggle/working/blender_{i}.log', 'w'), stderr=subprocess.STDOUT))
for p in procs:
    p.wait()
logs = "".join(open(f).read() for f in glob.glob(f'{out}/render_log_*.txt'))
open('/kaggle/working/summary.txt', 'w').write(f"gpus={ngpu} wall_min={(time.time()-t0)/60:.1f}\n" + logs)
print(open('/kaggle/working/summary.txt').read())
for i in range(ngpu):
    L = open(f'/kaggle/working/blender_{i}.log').read().splitlines()
    open(f'/kaggle/working/blender_{i}.log', 'w').write("\n".join([l for l in L if 'Fra:' not in l and 'Sample' not in l][-300:]))
