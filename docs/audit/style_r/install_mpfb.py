# Install MPFB 2.0.18 (official extensions.blender.org package, sha256 verified) into bpy's user extensions. Owner approved 16 Nov.
import bpy, sys, addon_utils
zp = sys.argv[-1]
print(bpy.ops.extensions.package_install_files(filepath=zp, repo="user_default", enable_on_install=True))
print("enabled", addon_utils.enable("bl_ext.user_default.mpfb", default_set=True) is not None)
