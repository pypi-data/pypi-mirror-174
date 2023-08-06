from kfp.v2.dsl import component, Input, Output, Artifact


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/bytetrack_from_video",
    output_component_file="component.yaml",
)
def bytetrack_from_video(
    input_video: Input[Artifact],
    input_weights: Input[Artifact],
    # device: str = "gpu",  # Must be gpu or cpu
    output_file: Output[Artifact],
):
    from tools.demo_track import make_parser, main, get_exp

    has_gpu = True
    if has_gpu:
        args = make_parser().parse_args(
            [
                "video",
                "-f",
                "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
                "-c",
                input_weights.path,
                "--path",
                input_video.path,
                "--fp16",
                "--fuse",
                "--save_result",
            ]
        )
    else:
        args = make_parser().parse_args(
            [
                "video",
                "-f",
                "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
                "-c",
                "/ByteTrack/pretrained/bytetrack_x_mot17.pth.tar",
                "--device",
                "cpu",
                "--path",
                "/ByteTrack/friends-Scene-008.mp4",  # input_video.path,
                "--fuse",
                "--save_result",
            ]
        )

    exp = get_exp(args.exp_file, args.name)
    main(exp=exp, args=args)
