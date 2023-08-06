from hdmf import docval
from hdmf.utils import get_docval, popargs
from pynwb import register_class
from pynwb.ophys import ImageSegmentation


@register_class("EXTRACTSegmentation", "ndx-extract")
class EXTRACTSegmentation(ImageSegmentation):
    """EXTRACT configuration parameters added to an ImageSegmentation object."""

    __nwbfields__ = (
        "version",
        "preprocess",
        "pre_mask_on",
        "pre_mask_radius",
        "fix_zero_FOV_strips",
        "medfilt_outlier_pixels",
        "skip_dff",
        "second_df",
        "skip_highpass",
        "spatial_highpass_cutoff",
        "temporal_denoising",
        "remove_background",
        "use_default_gpu",
        "use_gpu",
        "multi_gpu",
        "parallel_cpu",
        "avg_cell_radius",
        "avg_event_tau",
        "avg_yield_threshold",
        "num_partitions_x",
        "num_partitions_y",
        "trace_output_option",
        "trace_quantile",
        "dendrite_aware",
        "crop_circular",
        "use_sparse_arrays",
        "verbose",
        "compact_output",
        "hyperparameter_tuning_flag",
        "remove_duplicate_cells",
        "max_iter",
        "minimal_checks",
        "cellfind_min_snr",
        "cellfind_max_steps",
        "cellfind_kappa_std_ratio",
        "cellfind_filter_type",
        "cellfind_numpix_threshold",
        "cellfind_adaptive_kappa",
        "cellfind_spatial_highpass_cutoff",
        "moving_radius",
        "moving_radius_spatial",
        "moving_radius_temporal",
        "init_with_gaussian",
        "high2low_brightness_ratio",
        "visualize_cellfinding",
        "visualize_cellfinding_full_range",
        "visualize_cellfinding_max",
        "visualize_cellfinding_min",
        "visualize_cellfinding_show_bad_cells",
        "kappa_std_ratio",
        "T_dup_corr_thresh",
        "T_dup_thresh",
        "S_dup_corr_thresh",
        "S_corr_thresh",
        "T_corr_thresh",
        "temporal_corrupt_thresh",
        "spatial_corrupt_thresh",
        "T_min_snr",
        "size_lower_limit",
        "size_upper_limit",
        "eccent_thresh",
        "low_ST_index_thresh",
        "low_cell_area_flag",
        "high_ST_index_thresh",
        "low_ST_corr_thresh",
        "confidence_thresh",
        "downsample_time_by",
        "min_tau_after_downsampling",
        "downsample_space_by",
        "min_radius_after_downsampling",
        "reestimate_S_if_downsampled",
        "reestimate_T_if_downsampled",
        "adaptive_kappa",
        "arbitrary_mask",
        "smoothing_ratio_x2y",
        "spatial_lowpass_cutoff",
        "smooth_T",
        "smooth_S",
        "l1_penalty_factor",
        "max_iter_S",
        "max_iter_T",
        "TOL_sub",
        "TOL_main",
        "T_lower_snr_threshold",
        "save_all_found",
        "plot_loss",
        "baseline_quantile",
        "S_init",
        "T_init",
        "movie_mask",
        "is_pixel_valid",
        "num_frames",
        "num_iter_stop_quality_checks",
        "pick_gpu",
    )

    @docval(
        *get_docval(
            ImageSegmentation.__init__,
            "name",
        ),  # required
        {
            "name": "version",
            "type": str,
            "doc": "The version of EXTRACT.",
            "default": None,
        },
        {
            "name": "preprocess",
            "type": bool,
            "doc": "Indicates whether or not data preprocessing was applied before main EXTRACT function.",
            "default": None,
        },
        {
            "name": "pre_mask_on",
            "type": bool,
            "doc": "Indicates whether or not an image mask was applied for preprocessing.",
            "default": None,
        },
        {
            "name": "pre_mask_radius",
            "type": float,
            "doc": "If an image mask was applied for preprocessing, indicates the radius of the image mask.",
            "default": None,
        },
        {
            "name": "fix_zero_FOV_strips",
            "type": bool,
            "doc": "Indicates whether or not find and fix spatial slices that are occasionally zero due to "
            "frame registration during preprocessing.",
            "default": None,
        },
        {
            "name": "medfilt_outlier_pixels",
            "type": bool,
            "doc": "Determines whether outlier pixels in the movie should be replaced with their "
            "neighborhood median.",
            "default": None,
        },
        {
            "name": "skip_dff",
            "type": bool,
            "doc": "Indicates whether to skip Df/F calculation in preprocessing.",
            "default": None,
        },
        {
            "name": "second_df",
            "type": float,
            "doc": "The setting for second df calculation.",
            "default": None,
        },
        {
            "name": "skip_highpass",
            "type": bool,
            "doc": "Indicates whether to skip highpass filtering in preprocessing.",
            "default": None,
        },
        {
            "name": "spatial_highpass_cutoff",
            "type": float,
            "doc": "Cutoff determining the strength of butterworth spatial filtering of the movie. "
            "Values defined relative to the average cell radius.",
            "default": None,
        },
        {
            "name": "temporal_denoising",
            "type": bool,
            "doc": "Determines whether to apply temporal wavelet denoising.",
            "default": None,
        },
        {
            "name": "remove_background",
            "type": bool,
            "doc": "Determines whether to subtract the (spatial) background "
            "(largest spatiotemporal mode of the movie matrix).",
            "default": None,
        },
        {
            "name": "use_default_gpu",
            "type": bool,
            "doc": "Indicates whether or not use the default GPU.",
            "default": None,
        },
        {
            "name": "use_gpu",
            "type": bool,
            "doc": "Indicates whether to run EXTRACT on GPU. If False, EXTRACT was run on CPU.",
            "default": None,
        },
        {
            "name": "multi_gpu",
            "type": bool,
            "doc": "Indicates whether multiple GPUs were used.",
            "default": None,
        },
        {
            "name": "parallel_cpu",
            "type": bool,
            "doc": "Indicates whether parallel CPUs were used.",
            "default": None,
        },
        {
            "name": "avg_cell_radius",
            "type": float,
            "doc": "Radius estimate for an average cell in the movie.",
            "default": None,
        },
        {
            "name": "avg_event_tau",
            "type": float,
            "doc": "Determines the average event tau.",
            "default": None,
        },
        {
            "name": "avg_yield_threshold",
            "type": float,
            "doc": "Determines the average yield threshold.",
            "default": None,
        },
        {
            "name": "num_partitions_x",
            "type": float,
            "doc": "Number of movie partitions in x dimension.",
            "default": None,
        },
        {
            "name": "num_partitions_y",
            "type": float,
            "doc": "Number of movie partitions in y dimension.",
            "default": None,
        },
        {
            "name": "trace_output_option",
            "type": str,
            "doc": "Raw or non-negative output traces.",
            "default": None,
        },
        {
            "name": "trace_quantile",
            "type": float,
            "doc": "No description available.",
            "default": None,
        },
        {
            "name": "dendrite_aware",
            "type": bool,
            "doc": "Determines whether or not dendrites are preserved in the output "
            "for movies where dendrites are present.",
            "default": None,
        },
        {
            "name": "crop_circular",
            "type": bool,
            "doc": "For microendoscopic movies, whether or not automatically cropping out "
            "the region outside the circular imaging region.",
            "default": None,
        },
        {
            "name": "use_sparse_arrays",
            "type": bool,
            "doc": "Determines whether not the output cell images were saved as sparse arrays.",
            "default": None,
        },
        {
            "name": "verbose",
            "type": float,
            "doc": "Indicates the level of verbosity.",
            "default": None,
        },
        {
            "name": "compact_output",
            "type": bool,
            "doc": "Indicates whether or not leave out bad components that were found but "
            "then eliminated from the output.",
            "default": None,
        },
        {
            "name": "hyperparameter_tuning_flag",
            "type": bool,
            "doc": "Indicates whether or not use internal hyperparameter tuning.",
            "default": None,
        },
        {
            "name": "remove_duplicate_cells",
            "type": bool,
            "doc": "For movies processed in multiple partitions, "
            "this flag controls duplicate removal in the overlap regions.",
            "default": None,
        },
        {
            "name": "max_iter",
            "type": float,
            "doc": "Maximum number of alternating estimation iterations.",
            "default": None,
        },
        {
            "name": "minimal_checks",
            "type": float,
            "doc": "Minimum number of checks that are performed.",
            "default": None,
        },
        {
            "name": "cellfind_min_snr",
            "type": float,
            "doc": "Minimum peak SNR value for an object to be considered as a cell.",
            "default": None,
        },
        {
            "name": "cellfind_max_steps",
            "type": float,
            "doc": "Maximum number of cell candidate initialization during cell finding step.",
            "default": None,
        },
        {
            "name": "cellfind_kappa_std_ratio",
            "type": float,
            "doc": "Kappa will be set to this times the noise std for the component-wise EXTRACT during initialization.",
            "default": None,
        },
        {
            "name": "cellfind_filter_type",
            "type": str,
            "doc": "Type of the spatial smoothing filter used for cell finding.",
            "default": None,
        },
        {
            "name": "cellfind_numpix_threshold",
            "type": float,
            "doc": "During cell finding, objects with an area < cellfind_numpix_threshold are discarded.",
            "default": None,
        },
        {
            "name": "cellfind_adaptive_kappa",
            "type": bool,
            "doc": "If True, then during cell finding, the robust esimation loss will adaptively "
            "set its robustness parameter",
            "default": None,
        },
        {
            "name": "cellfind_spatial_highpass_cutoff",
            "type": float,
            "doc": "Cutoff determining the strength of butterworth spatial filtering of the movie. "
            "Values defined relative to the average cell radius. ",
            "default": None,
        },
        {
            "name": "moving_radius",
            "type": float,
            "doc": "Deprecated variable for older EXTRACT file versions. "
            "Radius of moving average filter in the case when cellfind_filter_type = moveavg "
            "(moving average)",
            "default": None,
        },
        {
            "name": "moving_radius_spatial",
            "type": float,
            "doc": "Radius of moving average filter in the case when cellfind_filter_type = moveavg "
            "(moving average) for the image.",
            "default": None,
        },
        {
            "name": "moving_radius_temporal",
            "type": float,
            "doc": "Radius of moving average filter in the case when cellfind_filter_type = moveavg "
            "(moving average) for the traces.",
            "default": None,
        },
        {
            "name": "init_with_gaussian",
            "type": bool,
            "doc": "If True, then during cell finding, each cell is initialized with a gaussian shape "
            "prior to robust estimation. If False, then initialization is done with a "
            "correlation image (preferred for movies with dendrites).",
            "default": None,
        },
        {
            "name": "high2low_brightness_ratio",
            "type": float,
            "doc": "Threshold for ratio of pixel compared to most bright region in FOV. Used to determine when to "
            "stop cell finding process.",
            "default": None,
        },
        {
            "name": "visualize_cellfinding",
            "type": float,
            "doc": "The visualization setting for cell finding.",
            "default": None,
        },
        {
            "name": "visualize_cellfinding_full_range",
            "type": float,
            "doc": "The visualization setting for cell finding.",
            "default": None,
        },
        {
            "name": "visualize_cellfinding_max",
            "type": float,
            "doc": "The visualization setting for cell finding.",
            "default": None,
        },
        {
            "name": "visualize_cellfinding_min",
            "type": float,
            "doc": "The visualization setting for cell finding.",
            "default": None,
        },
        {
            "name": "visualize_cellfinding_show_bad_cells",
            "type": float,
            "doc": "The visualization setting for cell finding.",
            "default": None,
        },
        {
            "name": "kappa_std_ratio",
            "type": float,
            "doc": "Kappa will be set to this times the noise std during the cell refinement process. "
            "Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "T_dup_corr_thresh",
            "type": float,
            "doc": "Through alternating estimation, cells that have higher trace correlation than T_dup_corr_thresh "
            "are eliminated. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "T_dup_thresh",
            "type": float,
            "doc": "Threshold for traces. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "S_dup_corr_thresh",
            "type": float,
            "doc": "Through alternating estimation, cells that have higher image correlation than S_dup_corr_thresh "
            "are eliminated. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "S_corr_thresh",
            "type": float,
            "doc": "Image correlation threshold. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "T_corr_thresh",
            "type": float,
            "doc": "Trace correlation threshold. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "temporal_corrupt_thresh",
            "type": float,
            "doc": "Threshold for temporal corruption index. Traces above this threshold are eliminated duirng "
            "alternating minimization routine. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "spatial_corrupt_thresh",
            "type": float,
            "doc": "Threshold for spatial corruption index. Images above this threshold are eliminated duirng "
            "alternating minimization routine. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "T_min_snr",
            "type": float,
            "doc": "Threshold for temporal SNR. Cells with temporal SNR below this value will be eliminated. "
            "Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "size_lower_limit",
            "type": float,
            "doc": "Lower size limit for found cells. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "size_upper_limit",
            "type": float,
            "doc": "Lower size limit for found cells. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "eccent_thresh",
            "type": float,
            "doc": "Upper limit of eccentricity for found cells. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "low_ST_index_thresh",
            "type": float,
            "doc": "Lower limit of spatiotemporal activity index. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "low_cell_area_flag",
            "type": bool,
            "doc": "Boolean flag indicating lower limit of cell area.",
            "default": None,
        },
        {
            "name": "high_ST_index_thresh",
            "type": float,
            "doc": "Upper limit limit of spatiotemporal activity index. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "low_ST_corr_thresh",
            "type": float,
            "doc": "Lower limit of spatiotemporal corelation. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "confidence_thresh",
            "type": float,
            "doc": "Confidence threshold for found cells. Cell refinement parameter.",
            "default": None,
        },
        {
            "name": "downsample_time_by",
            "type": float,
            "doc": "Time downsampling factor.",
            "default": None,
        },
        {
            "name": "min_tau_after_downsampling",
            "type": float,
            "doc": "Minimum event tau after downsampling.",
            "default": None,
        },
        {
            "name": "downsample_space_by",
            "type": float,
            "doc": "Spatial downsampling factor.",
            "default": None,
        },
        {
            "name": "min_radius_after_downsampling",
            "type": float,
            "doc": "Minimum avg radius after downsampling.",
            "default": None,
        },
        {
            "name": "reestimate_S_if_downsampled",
            "type": bool,
            "doc": "Boolean flag. When set to True, images are re-estimated from full movie at the end. "
            "When False, images are upsampled by interpolation.",
            "default": None,
        },
        {
            "name": "reestimate_T_if_downsampled",
            "type": bool,
            "doc": "Boolean flag. When set to True, traces are re-estimated from full movie at the end. "
            "When False, traces are upsampled by interpolation.",
            "default": None,
        },
        {
            "name": "adaptive_kappa",
            "type": bool,
            "doc": "Boolean flag. If True, then during cell finding, the robust esimation loss will adaptively "
            "set its robustness parameter",
            "default": None,
        },
        {
            "name": "arbitrary_mask",
            "type": bool,
            "doc": "Indicates whether to use an arbitrary mask on the image.",
            "default": None,
        },
        {
            "name": "smoothing_ratio_x2y",
            "type": float,
            "doc": "If the movie contains mainly objects that are elongated in one dimension "
            "(e.g. dendrites), this parameter is useful for more smoothing in either x or y dimension.",
            "default": None,
        },
        {
            "name": "spatial_lowpass_cutoff",
            "type": float,
            "doc": "Cutoff determining the strength of butterworth spatial filtering of the movie. "
            "Values defined relative to the average cell radius.",
            "default": None,
        },
        {
            "name": "smooth_T",
            "type": bool,
            "doc": "Indicates whether calculated traces are smoothed using median filtering.",
            "default": None,
        },
        {
            "name": "smooth_S",
            "type": bool,
            "doc": "Indicates whether calculated images are smoothed using a 2-D Gaussian filter.",
            "default": None,
        },
        {
            "name": "l1_penalty_factor",
            "type": float,
            "doc": "Strength of l1 regularization penalty to be applied when estimating the temporal components.",
            "default": None,
        },
        {
            "name": "max_iter_S",
            "type": float,
            "doc": "Maximum number of iterations for S estimation steps.",
            "default": None,
        },
        {
            "name": "max_iter_T",
            "type": float,
            "doc": "Maximum number of iterations for T estimation steps.",
            "default": None,
        },
        {
            "name": "TOL_sub",
            "type": float,
            "doc": "If the 1-step relative change in the objective within each T and S optimization is less than this, "
            "the respective optimization is terminated.",
            "default": None,
        },
        {
            "name": "TOL_main",
            "type": float,
            "doc": "If the relative change in the main objective function between 2 consecutive alternating "
            "minimization steps is less than this, cell extraction is terminated.",
            "default": None,
        },
        {
            "name": "T_lower_snr_threshold",
            "type": float,
            "doc": "Lower SNR threshold for found traces.",
            "default": None,
        },
        {
            "name": "save_all_found",
            "type": bool,
            "doc": "Determines whether to save all spatial and temporal components found.",
            "default": None,
        },
        {
            "name": "plot_loss",
            "type": bool,
            "doc": "Indicates whether empirical risk was plotted against iterations during alternating estimation.",
            "default": None,
        },
        {
            "name": "baseline_quantile",
            "type": ("array_data", "data"),
            "doc": "Baseline quantile for Df/F calculation in preprocessing."
            "The first dimension denotes the height of the image, the second dimension "
            "corresponds to the width of the image.",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "S_init",
            "type": ("array_data", "data"),
            "doc": "Cell images provided to algorithm as the initial set of cells, skipping its native initialization."
            "The first dimension denotes the height of the image, the second dimension "
            "corresponds to the width of the image.",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "T_init",
            "type": ("array_data", "data"),
            "doc": "Cell traces provided to algorithm as the initial set of traces, skipping its native initialization."
            "The first dimension denotes the number of cells, the second dimension "
            "corresponds to time.",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "movie_mask",
            "type": ("array_data", "data"),
            "doc": "The circular mask to apply for microendoscopic movies during preprocessing.",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "is_pixel_valid",
            "type": ("array_data", "data"),
            "doc": "No description available",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "num_frames",
            "type": ("array_data", "data"),
            "doc": "No description available",
            "default": None,
        },
        {
            "name": "num_iter_stop_quality_checks",
            "type": ("array_data", "data"),
            "doc": "No description available",
            "default": None,
            "shape": (None, None),
        },
        {
            "name": "pick_gpu",
            "type": ("array_data", "data"),
            "doc": "No description available",
            "default": None,
            "shape": (None, None),
        },
    )
    def __init__(self, **kwargs):
        name = popargs("name", kwargs)
        super().__init__(name=name)
        for extract_config_name, extract_config_value in kwargs.items():
            setattr(self, extract_config_name, extract_config_value)
