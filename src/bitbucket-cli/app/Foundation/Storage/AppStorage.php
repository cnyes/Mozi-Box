<?php

namespace App\Foundation\Storage;

use Illuminate\Filesystem\FilesystemManager;

class AppStorage extends FilesystemManager
{
    const TMP_PREFIX = "tmp";

    public function putTmp($path, $contents, $lock = false): bool
    {
        return $this->put(self::TMP_PREFIX . DIRECTORY_SEPARATOR . $path, $contents, $lock);
    }

    public function deleteTmp($paths): bool
    {
        $paths = is_array($paths) ? $paths : func_get_args();

        foreach ($paths as $key => $path) {
            $paths[$key] = self::TMP_PREFIX . DIRECTORY_SEPARATOR . $path;
        }

        return $this->delete($paths);
    }
}
