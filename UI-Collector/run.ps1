# $condaPath = (conda info --base)
# Invoke-Expression "$condaPath/etc/profile.d/conda.sh"
# conda activate py310
$pkgName=$args[0]
$appName=$args[1]
$depth=$args[2]
python run.py $pkgName $appName $depth