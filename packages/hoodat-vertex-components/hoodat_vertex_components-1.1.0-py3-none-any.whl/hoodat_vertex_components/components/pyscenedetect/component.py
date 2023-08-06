from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/pyscenedetect",
    output_component_file="component.yaml",
)
def pyscenedetect(
    input_video: Input[Artifact],
    output_stats: Output[Dataset],
    output_video_dir: Output[Artifact],
):
    import os
    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import ContentDetector
    from scenedetect.stats_manager import StatsManager
    from scenedetect.video_splitter import split_video_ffmpeg

    def split_video_into_scenes(
        video_path, output_stats_path, output_video_dir_path, threshold=27.0
    ):
        # Open the video, create a scene manager, and add a detector.
        video = open_video(video_path)
        stats_manager = StatsManager()
        # Construct the SceneManager and pass it the StatsManager.
        scene_manager = SceneManager(stats_manager)
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        scene_manager.detect_scenes(video, show_progress=True)
        scene_list = scene_manager.get_scene_list()
        os.makedirs(os.path.dirname(output_stats_path), exist_ok=True)
        stats_manager.save_to_csv(
            csv_file=output_stats_path, base_timecode=None, force_save=True
        )
        os.makedirs(output_video_dir_path)
        split_video_ffmpeg(
            input_video_path=video_path,
            scene_list=scene_list,
            output_file_template=os.path.join(
                output_video_dir_path, "$VIDEO_NAME-Scene-$SCENE_NUMBER.mp4"
            ),
            show_progress=True,
        )

    split_video_into_scenes(
        video_path=input_video.path,
        output_stats_path=output_stats.path,
        output_video_dir_path=output_video_dir.path,
    )
