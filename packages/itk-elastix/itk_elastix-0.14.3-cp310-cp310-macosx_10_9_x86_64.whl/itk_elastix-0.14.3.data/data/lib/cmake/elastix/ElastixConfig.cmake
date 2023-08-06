# ElastixConfig.cmake - Elastix CMake configuration file for external
# projects.
#

# This ElastixConfig file is  configured for the install
# tree.

# Compute this installation's prefix from this file's location:
get_filename_component(_ELASTIXConfig_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
set(Elastix_INSTALL_PREFIX "${_ELASTIXConfig_DIR}")
get_filename_component(Elastix_INSTALL_PREFIX "${Elastix_INSTALL_PREFIX}" PATH)
get_filename_component(Elastix_INSTALL_PREFIX "${Elastix_INSTALL_PREFIX}" PATH)
get_filename_component(Elastix_INSTALL_PREFIX "${Elastix_INSTALL_PREFIX}" PATH)

# Add include directories needed to use SuperElastix
set( ELASTIX_INCLUDE_DIRS ${Elastix_INSTALL_PREFIX}/include;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/CostFunctions;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/ImageSamplers;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/LineSearchOptimizers;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/ParameterFileParser;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/Transforms;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/xout;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Common/MevisDicomTiff;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core/Install;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core/Kernel;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core/ComponentBaseClasses;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core/Configuration;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Core/Main;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/FixedImagePyramids;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/ImageSamplers;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Interpolators;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Metrics;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/MovingImagePyramids;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Optimizers;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Registrations;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/ResampleInterpolators;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Resamplers;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/Components/Transforms;${Elastix_INSTALL_PREFIX}/include/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-build )

# Add list of Elastix library directories
set( ELASTIX_LIBRARY_DIRS "${Elastix_INSTALL_PREFIX}/lib" )

# Add list of SuperElastix libraries
set( ELASTIX_LIBRARIES elastix_lib;transformix_lib )

# The location of the Elastix use-file
set( ELASTIX_USE_FILE "${_ELASTIXConfig_DIR}/UseElastix.cmake" )

if(NOT ITK_CONFIG_TARGETS_FILE)
  find_package(ITK "5.3.0" EXACT REQUIRED)
endif()


# Import ELASTIX targets.
set( ELASTIX_CONFIG_TARGETS_FILE "${_ELASTIXConfig_DIR}/ElastixTargets.cmake")
list( GET ELASTIX_LIBRARIES 0 _first_library)
if(NOT ELASTIX_TARGETS_IMPORTED AND NOT TARGET ${_first_library})
  set(ELASTIX_TARGETS_IMPORTED 1)
  include("${ELASTIX_CONFIG_TARGETS_FILE}")
endif()


# Set some variables that the user might want to use
set( ELASTIX_USE_OPENMP ON )
set( ELASTIX_USE_OPENCL OFF )
set( ELASTIX_USE_MEVISDICOMTIFF OFF )

# FIXME - These variable refer to the source and build directories
set( ELASTIX_DOX_DIR /Users/runner/work/ITKElastix/ITKElastix/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-src/dox )
set( ELASTIX_HELP_DIR /Users/runner/work/ITKElastix/ITKElastix/_skbuild/macosx-10.9-universal2-3.10/cmake-build/_deps/elx-build/help )

# Maintain backwards compatibility by also exporting old-style target information
set( ELASTIX_ALL_COMPONENT_LIBS FixedGenericPyramid;FixedRecursivePyramid;FixedShrinkingPyramid;FixedSmoothingPyramid;FullSampler;GridSampler;MultiInputRandomCoordinateSampler;RandomSampler;RandomCoordinateSampler;RandomSamplerSparseMask;BSplineInterpolator;BSplineInterpolatorFloat;LinearInterpolator;NearestNeighborInterpolator;RayCastInterpolator;ReducedDimensionBSplineInterpolator;AdvancedKappaStatisticMetric;AdvancedMattesMutualInformationMetric;AdvancedMeanSquaresMetric;AdvancedNormalizedCorrelationMetric;TransformBendingEnergyPenalty;CorrespondingPointsEuclideanDistanceMetric;DisplacementMagnitudePenalty;DistancePreservingRigidityPenalty;GradientDifferenceMetric;MissingStructurePenalty;NormalizedGradientCorrelationMetric;NormalizedMutualInformationMetric;PCAMetric;PCAMetric2;PatternIntensityMetric;PolydataDummyPenalty;TransformRigidityPenalty;StatisticalShapePenalty;SumOfPairwiseCorrelationCoefficientsMetric;SumSquaredTissueVolumeDifferenceMetric;VarianceOverLastDimensionMetric;MovingGenericPyramid;MovingRecursivePyramid;MovingShrinkingPyramid;MovingSmoothingPyramid;AdaptiveStochasticGradientDescent;CMAEvolutionStrategy;ConjugateGradient;ConjugateGradientFRPR;FiniteDifferenceGradientDescent;FullSearch;Powell;PreconditionedStochasticGradientDescent;QuasiNewtonLBFGS;RSGDEachParameterApart;RegularStepGradientDescent;Simplex;SimultaneousPerturbation;StandardGradientDescent;MultiMetricMultiResolutionRegistration;MultiResolutionRegistration;MultiResolutionRegistrationWithFeatures;BSplineResampleInterpolator;BSplineResampleInterpolatorFloat;LinearResampleInterpolator;NearestNeighborResampleInterpolator;ReducedDimensionBSplineResampleInterpolator;RayCastResampleInterpolator;MyStandardResampler;AdvancedAffineTransformElastix;AdvancedBSplineTransform;AffineDTITransformElastix;AffineLogStackTransform;AffineLogTransformElastix;BSplineStackTransform;DeformationFieldTransform;EulerStackTransform;EulerTransformElastix;MultiBSplineTransformWithNormal;RecursiveBSplineTransform;SimilarityTransformElastix;SplineKernelTransform;TranslationStackTransform;TranslationTransformElastix;WeightedCombinationTransformElastix )
set( elxLIBRARY_DEPENDS_FILE  )
