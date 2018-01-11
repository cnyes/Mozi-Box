<?php

use App\Foundation\Storage\AppStorage;

if (!function_exists('app_local_path')) {

    function app_local_path($paths = null): string
    {
        $paths = is_array($paths) ? $paths : func_get_args();
        return join_path(array_merge([config('filesystems.disks.app_local.root')], $paths));
    }
}

if (!function_exists('app_local_tmp_path')) {

    function app_local_tmp_path($paths = null): string
    {
        $paths = is_array($paths) ? $paths : func_get_args();
        return join_path(array_merge([app_local_path(), AppStorage::TMP_PREFIX], $paths));
    }
}

if (!function_exists('join_path')) {
    function join_path(array $paths): string
    {
        $paths = is_array($paths) ? $paths : func_get_args();
        $paths = array_filter($paths, function ($path) {
            return !is_null($path);
        });

        return implode(DIRECTORY_SEPARATOR, $paths);
    }
}
