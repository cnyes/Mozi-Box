<?php

namespace Tests\Unit;

use App\Foundation\Storage\AppStorage;
use Illuminate\Filesystem\Filesystem;
use Tests\TestCase;

class AppStorageTest extends TestCase
{
    protected $storage = null;

    public function setUp(): void
    {
        parent::setUp();
        $this->storage = new AppStorage($this->app->getContainer());
    }

    public function testPutTmp()
    {
        $fileName = "diff.patch";
        $filePath = AppStorage::TMP_PREFIX . DIRECTORY_SEPARATOR . $fileName;
        $fileContent = "test diff";
        $this->fake();
        $this->storage->putTmp($fileName, $fileContent);

        $this->storage->assertExists($filePath);
        $this->assertEquals($this->storage->get($filePath), $fileContent);
    }

    public function testDeleteTmp()
    {
        $fileName = ["diff.patch", "diff2.patch", "diff3.patch"];
        $filePathPrefix = AppStorage::TMP_PREFIX . DIRECTORY_SEPARATOR;
        $fileContent = "test diff";

        $this->fake();

        $this->storage->putTmp($fileName[0], $fileContent);
        $this->storage->assertExists($filePathPrefix . $fileName[0]);

        $this->storage->deleteTmp($fileName[0]);
        $this->storage->assertMissing($filePathPrefix . $fileName[0]);

        $this->putTestingFiles($fileName, $filePathPrefix, "");
        $this->storage->deleteTmp($fileName);
        $this->assertMissingFiles($fileName, $filePathPrefix);

        $this->putTestingFiles($fileName, $filePathPrefix, "");
        $this->storage->deleteTmp($fileName[0], $fileName[1], $fileName[2]);
        $this->assertMissingFiles($fileName, $filePathPrefix);
    }

    protected function putTestingFiles($fileName, $filePathPrefix, $fileContent)
    {
        foreach ($fileName as $file) {
            $this->storage->putTmp($file, $fileContent);
            $this->storage->assertExists($filePathPrefix . $file);
        }
    }

    protected function assertMissingFiles($fileName, $filePathPrefix)
    {
        foreach ($fileName as $file) {
            $this->storage->assertMissing($filePathPrefix . $file);
        }
    }

    protected function fake($disk = null)
    {
        $disk = $disk ?: config('filesystems.default');

        (new Filesystem)->cleanDirectory(
            $root = storage_path('framework/testing/disks/' . $disk)
        );

        $this->storage->set($disk, $this->storage->createLocalDriver(['root' => $root]));
    }
}
