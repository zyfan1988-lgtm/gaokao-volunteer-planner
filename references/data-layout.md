# 本地数据约定

该 Skill 不发布原始录取数据。请只导入有权使用的公开文件、个人合法导出文件，或自行整理的表；在正式建议前回到官方页面核验。

数据根目录可使用以下约定：

```text
<data-root>/yifenyiduan_standard/sd_2026_culture_score_rank.csv
<data-root>/sdzk_2026_actual_results/sd_2026_regular_batch_admission_normalized.csv
```

一分一段表需要 `score` 与 `all_cumulative` 两列。投档表至少需要 `school`、`major_or_group`、`rank` 和 `round`；也兼容本项目山东标准化表中的 `college_name`、`major_name`、`minimum_rank`。建议再保留 `province`、`year`、`batch`、`subject_requirement`、`source_url`、`published_at`。

请不要把付费平台导出、含个人信息文件、未经授权的资料或整份受版权保护的 PDF 上传至公开仓库。
