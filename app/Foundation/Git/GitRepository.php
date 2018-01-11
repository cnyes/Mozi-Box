<?php

namespace App\Foundation\Git;

use Cz\Git\GitException;
use Cz\Git\GitRepository as BaseGitRepository;

class GitRepository extends BaseGitRepository
{
    public function applyDiff(string $diffFilePath): BaseGitRepository
    {
        $diffFilePath = $this->checkFileExists($diffFilePath);

        try {
            return $this->begin()->run('git apply', $diffFilePath)->end();
        } catch (GitException $ex) {
            throw new GitException('git apply failed.');
        }
    }

    public function checkBeforeApplyDiff(string $diffFilePath): BaseGitRepository
    {
        $diffFilePath = $this->checkFileExists($diffFilePath);

        try {
            return $this->begin()->run('git apply', '--check', $diffFilePath)->end();
        } catch (GitException $ex) {
            throw new GitException('git apply check failed.');
        }
    }

    public function checkFileExists(string $diffFilePath): string
    {
        if (!file_exists($diffFilePath)) {
            throw new GitException("diff path file is not exists.");
        }
        return realpath($diffFilePath);
    }
}
