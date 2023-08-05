/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace TF {
class _ArrayToListOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _EagerConstOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _FusedBatchNormExOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _FusedConv2DOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _FusedMatMulOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _HostRecvOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _HostSendOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _InternalTestMustExecuteTrait_;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _InternalTestNonResourceValueSideEffects_;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _ListToArrayOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _RecvOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _SendOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _TPUCompileMlirOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _TPUCompileMlirPlaceholderProgramKeyOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _TPUDeviceOrdinalPlaceholderOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _UnaryOpsCompositionOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _XlaHostComputeMlirOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _XlaRecvAtHostOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _XlaRecvAtHostV2Op;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _XlaSendFromHostOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _XlaSendFromHostV2Op;
} // namespace TF
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_ArrayToListOp declarations
//===----------------------------------------------------------------------===//

class _ArrayToListOpAdaptor {
public:
  _ArrayToListOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _ArrayToListOpAdaptor(_ArrayToListOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInput();
  ::mlir::ValueRange input();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _ArrayToListOp : public ::mlir::Op<_ArrayToListOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _ArrayToListOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("N"), ::llvm::StringRef("T"), ::llvm::StringRef("out_types")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr NAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr NAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getOutTypesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getOutTypesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr out_typesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr out_typesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._ArrayToList");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInput();
  ::mlir::Operation::operand_range input();
  ::mlir::MutableOperandRange getInputMutable();
  ::mlir::MutableOperandRange inputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getOutput();
  ::mlir::Operation::result_range output();
  size_t getN();
  size_t N();
  ::mlir::Type getT();
  ::mlir::Type T();
  mlir::ResultElementTypeRange getOutTypes();
  mlir::ResultElementTypeRange out_types();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_ArrayToListOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_EagerConstOp declarations
//===----------------------------------------------------------------------===//

class _EagerConstOpAdaptor {
public:
  _EagerConstOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _EagerConstOpAdaptor(_EagerConstOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getInput();
  ::mlir::Value input();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _EagerConstOp : public ::mlir::Op<_EagerConstOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _EagerConstOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._EagerConst");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getInput();
  ::mlir::TypedValue<::mlir::TensorType> input();
  ::mlir::MutableOperandRange getInputMutable();
  ::mlir::MutableOperandRange inputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getOutput();
  ::mlir::TypedValue<::mlir::TensorType> output();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type output, ::mlir::Value input);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value input);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_EagerConstOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_FusedBatchNormExOp declarations
//===----------------------------------------------------------------------===//

class _FusedBatchNormExOpAdaptor {
public:
  _FusedBatchNormExOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _FusedBatchNormExOpAdaptor(_FusedBatchNormExOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getX();
  ::mlir::Value x();
  ::mlir::Value getScale();
  ::mlir::Value scale();
  ::mlir::Value getOffset();
  ::mlir::Value offset();
  ::mlir::Value getMean();
  ::mlir::Value mean();
  ::mlir::Value getVariance();
  ::mlir::Value variance();
  ::mlir::ValueRange getSideInput();
  ::mlir::ValueRange side_input();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getExponentialAvgFactorAttr();
  ::llvm::APFloat getExponentialAvgFactor();
  ::mlir::FloatAttr exponential_avg_factorAttr();
  ::llvm::APFloat exponential_avg_factor();
  ::mlir::StringAttr getActivationModeAttr();
  ::llvm::StringRef getActivationMode();
  ::mlir::StringAttr activation_modeAttr();
  ::llvm::StringRef activation_mode();
  ::mlir::StringAttr getDataFormatAttr();
  ::llvm::StringRef getDataFormat();
  ::mlir::StringAttr data_formatAttr();
  ::llvm::StringRef data_format();
  ::mlir::BoolAttr getIsTrainingAttr();
  bool getIsTraining();
  ::mlir::BoolAttr is_trainingAttr();
  bool is_training();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _FusedBatchNormExOp : public ::mlir::Op<_FusedBatchNormExOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::NResults<6>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<5>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpAsmOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _FusedBatchNormExOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("U"), ::llvm::StringRef("activation_mode"), ::llvm::StringRef("data_format"), ::llvm::StringRef("epsilon"), ::llvm::StringRef("exponential_avg_factor"), ::llvm::StringRef("is_training"), ::llvm::StringRef("num_side_inputs")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getUAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getUAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr UAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr UAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getActivationModeAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getActivationModeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr activation_modeAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr activation_modeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getDataFormatAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getDataFormatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr data_formatAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr data_formatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getEpsilonAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getEpsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr epsilonAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr epsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getExponentialAvgFactorAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getExponentialAvgFactorAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr exponential_avg_factorAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr exponential_avg_factorAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr getIsTrainingAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr getIsTrainingAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  ::mlir::StringAttr is_trainingAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr is_trainingAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  ::mlir::StringAttr getNumSideInputsAttrName() {
    return getAttributeNameForIndex(7);
  }

  static ::mlir::StringAttr getNumSideInputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 7);
  }

  ::mlir::StringAttr num_side_inputsAttrName() {
    return getAttributeNameForIndex(7);
  }

  static ::mlir::StringAttr num_side_inputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 7);
  }

  void getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn);
  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._FusedBatchNormEx");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getX();
  ::mlir::TypedValue<::mlir::TensorType> x();
  ::mlir::TypedValue<::mlir::TensorType> getScale();
  ::mlir::TypedValue<::mlir::TensorType> scale();
  ::mlir::TypedValue<::mlir::TensorType> getOffset();
  ::mlir::TypedValue<::mlir::TensorType> offset();
  ::mlir::TypedValue<::mlir::TensorType> getMean();
  ::mlir::TypedValue<::mlir::TensorType> mean();
  ::mlir::TypedValue<::mlir::TensorType> getVariance();
  ::mlir::TypedValue<::mlir::TensorType> variance();
  ::mlir::Operation::operand_range getSideInput();
  ::mlir::Operation::operand_range side_input();
  ::mlir::MutableOperandRange getXMutable();
  ::mlir::MutableOperandRange xMutable();
  ::mlir::MutableOperandRange getScaleMutable();
  ::mlir::MutableOperandRange scaleMutable();
  ::mlir::MutableOperandRange getOffsetMutable();
  ::mlir::MutableOperandRange offsetMutable();
  ::mlir::MutableOperandRange getMeanMutable();
  ::mlir::MutableOperandRange meanMutable();
  ::mlir::MutableOperandRange getVarianceMutable();
  ::mlir::MutableOperandRange varianceMutable();
  ::mlir::MutableOperandRange getSideInputMutable();
  ::mlir::MutableOperandRange side_inputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getY();
  ::mlir::TypedValue<::mlir::TensorType> y();
  ::mlir::TypedValue<::mlir::TensorType> getBatchMean();
  ::mlir::TypedValue<::mlir::TensorType> batch_mean();
  ::mlir::TypedValue<::mlir::TensorType> getBatchVariance();
  ::mlir::TypedValue<::mlir::TensorType> batch_variance();
  ::mlir::TypedValue<::mlir::TensorType> getReserveSpace_1();
  ::mlir::TypedValue<::mlir::TensorType> reserve_space_1();
  ::mlir::TypedValue<::mlir::TensorType> getReserveSpace_2();
  ::mlir::TypedValue<::mlir::TensorType> reserve_space_2();
  ::mlir::TypedValue<::mlir::TensorType> getReserveSpace_3();
  ::mlir::TypedValue<::mlir::TensorType> reserve_space_3();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getExponentialAvgFactorAttr();
  ::llvm::APFloat getExponentialAvgFactor();
  ::mlir::FloatAttr exponential_avg_factorAttr();
  ::llvm::APFloat exponential_avg_factor();
  ::mlir::StringAttr getActivationModeAttr();
  ::llvm::StringRef getActivationMode();
  ::mlir::StringAttr activation_modeAttr();
  ::llvm::StringRef activation_mode();
  ::mlir::StringAttr getDataFormatAttr();
  ::llvm::StringRef getDataFormat();
  ::mlir::StringAttr data_formatAttr();
  ::llvm::StringRef data_format();
  ::mlir::BoolAttr getIsTrainingAttr();
  bool getIsTraining();
  ::mlir::BoolAttr is_trainingAttr();
  bool is_training();
  size_t getNumSideInputs();
  size_t num_side_inputs();
  ::mlir::Type getT();
  ::mlir::Type T();
  ::mlir::Type getU();
  ::mlir::Type U();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setEpsilonAttr(::mlir::FloatAttr attr);
  void setEpsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void epsilonAttr(::mlir::FloatAttr attr);
  void epsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void setExponentialAvgFactorAttr(::mlir::FloatAttr attr);
  void setExponentialAvgFactor(::llvm::Optional<::llvm::APFloat> attrValue);
  void exponential_avg_factorAttr(::mlir::FloatAttr attr);
  void exponential_avg_factor(::llvm::Optional<::llvm::APFloat> attrValue);
  void setActivationModeAttr(::mlir::StringAttr attr);
  void setActivationMode(::llvm::Optional<::llvm::StringRef> attrValue);
  void activation_modeAttr(::mlir::StringAttr attr);
  void activation_mode(::llvm::Optional<::llvm::StringRef> attrValue);
  void setDataFormatAttr(::mlir::StringAttr attr);
  void setDataFormat(::llvm::Optional<::llvm::StringRef> attrValue);
  void data_formatAttr(::mlir::StringAttr attr);
  void data_format(::llvm::Optional<::llvm::StringRef> attrValue);
  void setIsTrainingAttr(::mlir::BoolAttr attr);
  void setIsTraining(::llvm::Optional<bool> attrValue);
  void is_trainingAttr(::mlir::BoolAttr attr);
  void is_training(::llvm::Optional<bool> attrValue);
  ::mlir::Attribute removeEpsilonAttr();
  ::mlir::Attribute removeExponential_avg_factorAttr();
  ::mlir::Attribute removeActivation_modeAttr();
  ::mlir::Attribute removeData_formatAttr();
  ::mlir::Attribute removeIs_trainingAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type y, ::mlir::Type batch_mean, ::mlir::Type batch_variance, ::mlir::Type reserve_space_1, ::mlir::Type reserve_space_2, ::mlir::Type reserve_space_3, ::mlir::Value x, ::mlir::Value scale, ::mlir::Value offset, ::mlir::Value mean, ::mlir::Value variance, ::mlir::ValueRange side_input, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr exponential_avg_factor, /*optional*/::mlir::StringAttr activation_mode, /*optional*/::mlir::StringAttr data_format, /*optional*/::mlir::BoolAttr is_training);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value x, ::mlir::Value scale, ::mlir::Value offset, ::mlir::Value mean, ::mlir::Value variance, ::mlir::ValueRange side_input, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr exponential_avg_factor, /*optional*/::mlir::StringAttr activation_mode, /*optional*/::mlir::StringAttr data_format, /*optional*/::mlir::BoolAttr is_training);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type y, ::mlir::Type batch_mean, ::mlir::Type batch_variance, ::mlir::Type reserve_space_1, ::mlir::Type reserve_space_2, ::mlir::Type reserve_space_3, ::mlir::Value x, ::mlir::Value scale, ::mlir::Value offset, ::mlir::Value mean, ::mlir::Value variance, ::mlir::ValueRange side_input, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat exponential_avg_factor, /*optional*/::llvm::StringRef activation_mode = "Identity", /*optional*/::llvm::StringRef data_format = "NHWC", /*optional*/bool is_training = true);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value x, ::mlir::Value scale, ::mlir::Value offset, ::mlir::Value mean, ::mlir::Value variance, ::mlir::ValueRange side_input, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat exponential_avg_factor, /*optional*/::llvm::StringRef activation_mode = "Identity", /*optional*/::llvm::StringRef data_format = "NHWC", /*optional*/bool is_training = true);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 8 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_FusedBatchNormExOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_FusedConv2DOp declarations
//===----------------------------------------------------------------------===//

class _FusedConv2DOpAdaptor {
public:
  _FusedConv2DOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _FusedConv2DOpAdaptor(_FusedConv2DOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getInput();
  ::mlir::Value input();
  ::mlir::Value getFilter();
  ::mlir::Value filter();
  ::mlir::ValueRange getArgs();
  ::mlir::ValueRange args();
  ::mlir::ValueRange getHostArgs();
  ::mlir::ValueRange host_args();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getNumArgsAttr();
  uint64_t getNumArgs();
  ::mlir::IntegerAttr num_argsAttr();
  uint64_t num_args();
  ::mlir::ArrayAttr getStridesAttr();
  ::mlir::ArrayAttr getStrides();
  ::mlir::ArrayAttr stridesAttr();
  ::mlir::ArrayAttr strides();
  ::mlir::StringAttr getPaddingAttr();
  ::llvm::StringRef getPadding();
  ::mlir::StringAttr paddingAttr();
  ::llvm::StringRef padding();
  ::mlir::ArrayAttr getExplicitPaddingsAttr();
  ::mlir::ArrayAttr getExplicitPaddings();
  ::mlir::ArrayAttr explicit_paddingsAttr();
  ::mlir::ArrayAttr explicit_paddings();
  ::mlir::StringAttr getDataFormatAttr();
  ::llvm::StringRef getDataFormat();
  ::mlir::StringAttr data_formatAttr();
  ::llvm::StringRef data_format();
  ::mlir::StringAttr getFilterFormatAttr();
  ::llvm::StringRef getFilterFormat();
  ::mlir::StringAttr filter_formatAttr();
  ::llvm::StringRef filter_format();
  ::mlir::ArrayAttr getDilationsAttr();
  ::mlir::ArrayAttr getDilations();
  ::mlir::ArrayAttr dilationsAttr();
  ::mlir::ArrayAttr dilations();
  ::mlir::BoolAttr getUseCudnnOnGpuAttr();
  bool getUseCudnnOnGpu();
  ::mlir::BoolAttr use_cudnn_on_gpuAttr();
  bool use_cudnn_on_gpu();
  ::mlir::ArrayAttr getFusedOpsAttr();
  ::mlir::ArrayAttr getFusedOps();
  ::mlir::ArrayAttr fused_opsAttr();
  ::mlir::ArrayAttr fused_ops();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getLeakyreluAlphaAttr();
  ::llvm::APFloat getLeakyreluAlpha();
  ::mlir::FloatAttr leakyrelu_alphaAttr();
  ::llvm::APFloat leakyrelu_alpha();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _FusedConv2DOp : public ::mlir::Op<_FusedConv2DOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _FusedConv2DOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("TArgs"), ::llvm::StringRef("data_format"), ::llvm::StringRef("dilations"), ::llvm::StringRef("epsilon"), ::llvm::StringRef("explicit_paddings"), ::llvm::StringRef("filter_format"), ::llvm::StringRef("fused_ops"), ::llvm::StringRef("leakyrelu_alpha"), ::llvm::StringRef("num_args"), ::llvm::StringRef("num_host_args"), ::llvm::StringRef("operand_segment_sizes"), ::llvm::StringRef("padding"), ::llvm::StringRef("strides"), ::llvm::StringRef("use_cudnn_on_gpu")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getTArgsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getTArgsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr TArgsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr TArgsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getDataFormatAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getDataFormatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr data_formatAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr data_formatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getDilationsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getDilationsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr dilationsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr dilationsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getEpsilonAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getEpsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr epsilonAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr epsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getExplicitPaddingsAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getExplicitPaddingsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr explicit_paddingsAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr explicit_paddingsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr getFilterFormatAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr getFilterFormatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  ::mlir::StringAttr filter_formatAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr filter_formatAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  ::mlir::StringAttr getFusedOpsAttrName() {
    return getAttributeNameForIndex(7);
  }

  static ::mlir::StringAttr getFusedOpsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 7);
  }

  ::mlir::StringAttr fused_opsAttrName() {
    return getAttributeNameForIndex(7);
  }

  static ::mlir::StringAttr fused_opsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 7);
  }

  ::mlir::StringAttr getLeakyreluAlphaAttrName() {
    return getAttributeNameForIndex(8);
  }

  static ::mlir::StringAttr getLeakyreluAlphaAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 8);
  }

  ::mlir::StringAttr leakyrelu_alphaAttrName() {
    return getAttributeNameForIndex(8);
  }

  static ::mlir::StringAttr leakyrelu_alphaAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 8);
  }

  ::mlir::StringAttr getNumArgsAttrName() {
    return getAttributeNameForIndex(9);
  }

  static ::mlir::StringAttr getNumArgsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 9);
  }

  ::mlir::StringAttr num_argsAttrName() {
    return getAttributeNameForIndex(9);
  }

  static ::mlir::StringAttr num_argsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 9);
  }

  ::mlir::StringAttr getNumHostArgsAttrName() {
    return getAttributeNameForIndex(10);
  }

  static ::mlir::StringAttr getNumHostArgsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 10);
  }

  ::mlir::StringAttr num_host_argsAttrName() {
    return getAttributeNameForIndex(10);
  }

  static ::mlir::StringAttr num_host_argsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 10);
  }

  ::mlir::StringAttr getOperandSegmentSizesAttrName() {
    return getAttributeNameForIndex(11);
  }

  static ::mlir::StringAttr getOperandSegmentSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 11);
  }

  ::mlir::StringAttr operand_segment_sizesAttrName() {
    return getAttributeNameForIndex(11);
  }

  static ::mlir::StringAttr operand_segment_sizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 11);
  }

  ::mlir::StringAttr getPaddingAttrName() {
    return getAttributeNameForIndex(12);
  }

  static ::mlir::StringAttr getPaddingAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 12);
  }

  ::mlir::StringAttr paddingAttrName() {
    return getAttributeNameForIndex(12);
  }

  static ::mlir::StringAttr paddingAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 12);
  }

  ::mlir::StringAttr getStridesAttrName() {
    return getAttributeNameForIndex(13);
  }

  static ::mlir::StringAttr getStridesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 13);
  }

  ::mlir::StringAttr stridesAttrName() {
    return getAttributeNameForIndex(13);
  }

  static ::mlir::StringAttr stridesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 13);
  }

  ::mlir::StringAttr getUseCudnnOnGpuAttrName() {
    return getAttributeNameForIndex(14);
  }

  static ::mlir::StringAttr getUseCudnnOnGpuAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 14);
  }

  ::mlir::StringAttr use_cudnn_on_gpuAttrName() {
    return getAttributeNameForIndex(14);
  }

  static ::mlir::StringAttr use_cudnn_on_gpuAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 14);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._FusedConv2D");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getInput();
  ::mlir::TypedValue<::mlir::TensorType> input();
  ::mlir::TypedValue<::mlir::TensorType> getFilter();
  ::mlir::TypedValue<::mlir::TensorType> filter();
  ::mlir::Operation::operand_range getArgs();
  ::mlir::Operation::operand_range args();
  ::mlir::Operation::operand_range getHostArgs();
  ::mlir::Operation::operand_range host_args();
  ::mlir::MutableOperandRange getInputMutable();
  ::mlir::MutableOperandRange inputMutable();
  ::mlir::MutableOperandRange getFilterMutable();
  ::mlir::MutableOperandRange filterMutable();
  ::mlir::MutableOperandRange getArgsMutable();
  ::mlir::MutableOperandRange argsMutable();
  ::mlir::MutableOperandRange getHostArgsMutable();
  ::mlir::MutableOperandRange host_argsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getOutput();
  ::mlir::TypedValue<::mlir::TensorType> output();
  ::mlir::IntegerAttr getNumArgsAttr();
  uint64_t getNumArgs();
  ::mlir::IntegerAttr num_argsAttr();
  uint64_t num_args();
  ::mlir::ArrayAttr getStridesAttr();
  ::mlir::ArrayAttr getStrides();
  ::mlir::ArrayAttr stridesAttr();
  ::mlir::ArrayAttr strides();
  ::mlir::StringAttr getPaddingAttr();
  ::llvm::StringRef getPadding();
  ::mlir::StringAttr paddingAttr();
  ::llvm::StringRef padding();
  ::mlir::ArrayAttr getExplicitPaddingsAttr();
  ::mlir::ArrayAttr getExplicitPaddings();
  ::mlir::ArrayAttr explicit_paddingsAttr();
  ::mlir::ArrayAttr explicit_paddings();
  ::mlir::StringAttr getDataFormatAttr();
  ::llvm::StringRef getDataFormat();
  ::mlir::StringAttr data_formatAttr();
  ::llvm::StringRef data_format();
  ::mlir::StringAttr getFilterFormatAttr();
  ::llvm::StringRef getFilterFormat();
  ::mlir::StringAttr filter_formatAttr();
  ::llvm::StringRef filter_format();
  ::mlir::ArrayAttr getDilationsAttr();
  ::mlir::ArrayAttr getDilations();
  ::mlir::ArrayAttr dilationsAttr();
  ::mlir::ArrayAttr dilations();
  ::mlir::BoolAttr getUseCudnnOnGpuAttr();
  bool getUseCudnnOnGpu();
  ::mlir::BoolAttr use_cudnn_on_gpuAttr();
  bool use_cudnn_on_gpu();
  ::mlir::ArrayAttr getFusedOpsAttr();
  ::mlir::ArrayAttr getFusedOps();
  ::mlir::ArrayAttr fused_opsAttr();
  ::mlir::ArrayAttr fused_ops();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getLeakyreluAlphaAttr();
  ::llvm::APFloat getLeakyreluAlpha();
  ::mlir::FloatAttr leakyrelu_alphaAttr();
  ::llvm::APFloat leakyrelu_alpha();
  size_t getNumHostArgs();
  size_t num_host_args();
  ::mlir::Type getT();
  ::mlir::Type T();
  mlir::OperandElementTypeRange getTArgs();
  mlir::OperandElementTypeRange TArgs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setNumArgsAttr(::mlir::IntegerAttr attr);
  void setNumArgs(uint64_t attrValue);
  void num_argsAttr(::mlir::IntegerAttr attr);
  void num_args(uint64_t attrValue);
  void setStridesAttr(::mlir::ArrayAttr attr);
  void stridesAttr(::mlir::ArrayAttr attr);
  void setPaddingAttr(::mlir::StringAttr attr);
  void setPadding(::llvm::StringRef attrValue);
  void paddingAttr(::mlir::StringAttr attr);
  void padding(::llvm::StringRef attrValue);
  void setExplicitPaddingsAttr(::mlir::ArrayAttr attr);
  void explicit_paddingsAttr(::mlir::ArrayAttr attr);
  void setDataFormatAttr(::mlir::StringAttr attr);
  void setDataFormat(::llvm::Optional<::llvm::StringRef> attrValue);
  void data_formatAttr(::mlir::StringAttr attr);
  void data_format(::llvm::Optional<::llvm::StringRef> attrValue);
  void setFilterFormatAttr(::mlir::StringAttr attr);
  void setFilterFormat(::llvm::Optional<::llvm::StringRef> attrValue);
  void filter_formatAttr(::mlir::StringAttr attr);
  void filter_format(::llvm::Optional<::llvm::StringRef> attrValue);
  void setDilationsAttr(::mlir::ArrayAttr attr);
  void dilationsAttr(::mlir::ArrayAttr attr);
  void setUseCudnnOnGpuAttr(::mlir::BoolAttr attr);
  void setUseCudnnOnGpu(::llvm::Optional<bool> attrValue);
  void use_cudnn_on_gpuAttr(::mlir::BoolAttr attr);
  void use_cudnn_on_gpu(::llvm::Optional<bool> attrValue);
  void setFusedOpsAttr(::mlir::ArrayAttr attr);
  void fused_opsAttr(::mlir::ArrayAttr attr);
  void setEpsilonAttr(::mlir::FloatAttr attr);
  void setEpsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void epsilonAttr(::mlir::FloatAttr attr);
  void epsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void setLeakyreluAlphaAttr(::mlir::FloatAttr attr);
  void setLeakyreluAlpha(::llvm::Optional<::llvm::APFloat> attrValue);
  void leakyrelu_alphaAttr(::mlir::FloatAttr attr);
  void leakyrelu_alpha(::llvm::Optional<::llvm::APFloat> attrValue);
  ::mlir::Attribute removeExplicit_paddingsAttr();
  ::mlir::Attribute removeData_formatAttr();
  ::mlir::Attribute removeFilter_formatAttr();
  ::mlir::Attribute removeDilationsAttr();
  ::mlir::Attribute removeUse_cudnn_on_gpuAttr();
  ::mlir::Attribute removeFused_opsAttr();
  ::mlir::Attribute removeEpsilonAttr();
  ::mlir::Attribute removeLeakyrelu_alphaAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type output, ::mlir::Value input, ::mlir::Value filter, ::mlir::ValueRange args, ::mlir::ValueRange host_args, ::mlir::IntegerAttr num_args, ::mlir::ArrayAttr strides, ::mlir::StringAttr padding, /*optional*/::mlir::ArrayAttr explicit_paddings, /*optional*/::mlir::StringAttr data_format, /*optional*/::mlir::StringAttr filter_format, /*optional*/::mlir::ArrayAttr dilations, /*optional*/::mlir::BoolAttr use_cudnn_on_gpu, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value input, ::mlir::Value filter, ::mlir::ValueRange args, ::mlir::ValueRange host_args, ::mlir::IntegerAttr num_args, ::mlir::ArrayAttr strides, ::mlir::StringAttr padding, /*optional*/::mlir::ArrayAttr explicit_paddings, /*optional*/::mlir::StringAttr data_format, /*optional*/::mlir::StringAttr filter_format, /*optional*/::mlir::ArrayAttr dilations, /*optional*/::mlir::BoolAttr use_cudnn_on_gpu, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type output, ::mlir::Value input, ::mlir::Value filter, ::mlir::ValueRange args, ::mlir::ValueRange host_args, uint64_t num_args, ::mlir::ArrayAttr strides, ::llvm::StringRef padding, /*optional*/::mlir::ArrayAttr explicit_paddings, /*optional*/::llvm::StringRef data_format, /*optional*/::llvm::StringRef filter_format, /*optional*/::mlir::ArrayAttr dilations, /*optional*/bool use_cudnn_on_gpu, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value input, ::mlir::Value filter, ::mlir::ValueRange args, ::mlir::ValueRange host_args, uint64_t num_args, ::mlir::ArrayAttr strides, ::llvm::StringRef padding, /*optional*/::mlir::ArrayAttr explicit_paddings, /*optional*/::llvm::StringRef data_format, /*optional*/::llvm::StringRef filter_format, /*optional*/::mlir::ArrayAttr dilations, /*optional*/bool use_cudnn_on_gpu, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat leakyrelu_alpha);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 15 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_FusedConv2DOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_FusedMatMulOp declarations
//===----------------------------------------------------------------------===//

class _FusedMatMulOpAdaptor {
public:
  _FusedMatMulOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _FusedMatMulOpAdaptor(_FusedMatMulOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getA();
  ::mlir::Value a();
  ::mlir::Value getB();
  ::mlir::Value b();
  ::mlir::ValueRange getArgs();
  ::mlir::ValueRange args();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr getTransposeAAttr();
  bool getTransposeA();
  ::mlir::BoolAttr transpose_aAttr();
  bool transpose_a();
  ::mlir::BoolAttr getTransposeBAttr();
  bool getTransposeB();
  ::mlir::BoolAttr transpose_bAttr();
  bool transpose_b();
  ::mlir::ArrayAttr getFusedOpsAttr();
  ::mlir::ArrayAttr getFusedOps();
  ::mlir::ArrayAttr fused_opsAttr();
  ::mlir::ArrayAttr fused_ops();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getLeakyreluAlphaAttr();
  ::llvm::APFloat getLeakyreluAlpha();
  ::mlir::FloatAttr leakyrelu_alphaAttr();
  ::llvm::APFloat leakyrelu_alpha();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _FusedMatMulOp : public ::mlir::Op<_FusedMatMulOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::TF::SameOperandsAndResultElementTypeResolveRef, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _FusedMatMulOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("epsilon"), ::llvm::StringRef("fused_ops"), ::llvm::StringRef("leakyrelu_alpha"), ::llvm::StringRef("num_args"), ::llvm::StringRef("transpose_a"), ::llvm::StringRef("transpose_b")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getEpsilonAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getEpsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr epsilonAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr epsilonAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getFusedOpsAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getFusedOpsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr fused_opsAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr fused_opsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getLeakyreluAlphaAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getLeakyreluAlphaAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr leakyrelu_alphaAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr leakyrelu_alphaAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getNumArgsAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getNumArgsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr num_argsAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr num_argsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getTransposeAAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getTransposeAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr transpose_aAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr transpose_aAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr getTransposeBAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr getTransposeBAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  ::mlir::StringAttr transpose_bAttrName() {
    return getAttributeNameForIndex(6);
  }

  static ::mlir::StringAttr transpose_bAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 6);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._FusedMatMul");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getA();
  ::mlir::TypedValue<::mlir::TensorType> a();
  ::mlir::TypedValue<::mlir::TensorType> getB();
  ::mlir::TypedValue<::mlir::TensorType> b();
  ::mlir::Operation::operand_range getArgs();
  ::mlir::Operation::operand_range args();
  ::mlir::MutableOperandRange getAMutable();
  ::mlir::MutableOperandRange aMutable();
  ::mlir::MutableOperandRange getBMutable();
  ::mlir::MutableOperandRange bMutable();
  ::mlir::MutableOperandRange getArgsMutable();
  ::mlir::MutableOperandRange argsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getProduct();
  ::mlir::TypedValue<::mlir::TensorType> product();
  ::mlir::BoolAttr getTransposeAAttr();
  bool getTransposeA();
  ::mlir::BoolAttr transpose_aAttr();
  bool transpose_a();
  ::mlir::BoolAttr getTransposeBAttr();
  bool getTransposeB();
  ::mlir::BoolAttr transpose_bAttr();
  bool transpose_b();
  ::mlir::ArrayAttr getFusedOpsAttr();
  ::mlir::ArrayAttr getFusedOps();
  ::mlir::ArrayAttr fused_opsAttr();
  ::mlir::ArrayAttr fused_ops();
  ::mlir::FloatAttr getEpsilonAttr();
  ::llvm::APFloat getEpsilon();
  ::mlir::FloatAttr epsilonAttr();
  ::llvm::APFloat epsilon();
  ::mlir::FloatAttr getLeakyreluAlphaAttr();
  ::llvm::APFloat getLeakyreluAlpha();
  ::mlir::FloatAttr leakyrelu_alphaAttr();
  ::llvm::APFloat leakyrelu_alpha();
  size_t getNumArgs();
  size_t num_args();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setTransposeAAttr(::mlir::BoolAttr attr);
  void setTransposeA(::llvm::Optional<bool> attrValue);
  void transpose_aAttr(::mlir::BoolAttr attr);
  void transpose_a(::llvm::Optional<bool> attrValue);
  void setTransposeBAttr(::mlir::BoolAttr attr);
  void setTransposeB(::llvm::Optional<bool> attrValue);
  void transpose_bAttr(::mlir::BoolAttr attr);
  void transpose_b(::llvm::Optional<bool> attrValue);
  void setFusedOpsAttr(::mlir::ArrayAttr attr);
  void fused_opsAttr(::mlir::ArrayAttr attr);
  void setEpsilonAttr(::mlir::FloatAttr attr);
  void setEpsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void epsilonAttr(::mlir::FloatAttr attr);
  void epsilon(::llvm::Optional<::llvm::APFloat> attrValue);
  void setLeakyreluAlphaAttr(::mlir::FloatAttr attr);
  void setLeakyreluAlpha(::llvm::Optional<::llvm::APFloat> attrValue);
  void leakyrelu_alphaAttr(::mlir::FloatAttr attr);
  void leakyrelu_alpha(::llvm::Optional<::llvm::APFloat> attrValue);
  ::mlir::Attribute removeTranspose_aAttr();
  ::mlir::Attribute removeTranspose_bAttr();
  ::mlir::Attribute removeFused_opsAttr();
  ::mlir::Attribute removeEpsilonAttr();
  ::mlir::Attribute removeLeakyrelu_alphaAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type product, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange args, /*optional*/::mlir::BoolAttr transpose_a, /*optional*/::mlir::BoolAttr transpose_b, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange args, /*optional*/::mlir::BoolAttr transpose_a, /*optional*/::mlir::BoolAttr transpose_b, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::mlir::FloatAttr epsilon, /*optional*/::mlir::FloatAttr leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type product, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange args, /*optional*/bool transpose_a, /*optional*/bool transpose_b, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat leakyrelu_alpha);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange args, /*optional*/bool transpose_a, /*optional*/bool transpose_b, /*optional*/::mlir::ArrayAttr fused_ops, /*optional*/::llvm::APFloat epsilon, /*optional*/::llvm::APFloat leakyrelu_alpha);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 7 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_FusedMatMulOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_HostRecvOp declarations
//===----------------------------------------------------------------------===//

class _HostRecvOpAdaptor {
public:
  _HostRecvOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _HostRecvOpAdaptor(_HostRecvOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _HostRecvOp : public ::mlir::Op<_HostRecvOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _HostRecvOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("client_terminated"), ::llvm::StringRef("recv_device"), ::llvm::StringRef("send_device"), ::llvm::StringRef("send_device_incarnation"), ::llvm::StringRef("tensor_name"), ::llvm::StringRef("tensor_type")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getClientTerminatedAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getClientTerminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr client_terminatedAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr client_terminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getRecvDeviceAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getRecvDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr recv_deviceAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr recv_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getSendDeviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getSendDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr send_deviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr send_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSendDeviceIncarnationAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSendDeviceIncarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr send_device_incarnationAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr send_device_incarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getTensorNameAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getTensorNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr tensor_nameAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr tensor_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getTensorTypeAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getTensorTypeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr tensor_typeAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr tensor_typeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._HostRecv");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getTensor();
  ::mlir::TypedValue<::mlir::TensorType> tensor();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::Type getTensorType();
  ::mlir::Type tensor_type();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setTensorNameAttr(::mlir::StringAttr attr);
  void setTensorName(::llvm::StringRef attrValue);
  void tensor_nameAttr(::mlir::StringAttr attr);
  void tensor_name(::llvm::StringRef attrValue);
  void setSendDeviceAttr(::mlir::StringAttr attr);
  void setSendDevice(::llvm::StringRef attrValue);
  void send_deviceAttr(::mlir::StringAttr attr);
  void send_device(::llvm::StringRef attrValue);
  void setSendDeviceIncarnationAttr(::mlir::IntegerAttr attr);
  void setSendDeviceIncarnation(uint64_t attrValue);
  void send_device_incarnationAttr(::mlir::IntegerAttr attr);
  void send_device_incarnation(uint64_t attrValue);
  void setRecvDeviceAttr(::mlir::StringAttr attr);
  void setRecvDevice(::llvm::StringRef attrValue);
  void recv_deviceAttr(::mlir::StringAttr attr);
  void recv_device(::llvm::StringRef attrValue);
  void setClientTerminatedAttr(::mlir::BoolAttr attr);
  void setClientTerminated(::llvm::Optional<bool> attrValue);
  void client_terminatedAttr(::mlir::BoolAttr attr);
  void client_terminated(::llvm::Optional<bool> attrValue);
  ::mlir::Attribute removeClient_terminatedAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 6 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_HostRecvOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_HostSendOp declarations
//===----------------------------------------------------------------------===//

class _HostSendOpAdaptor {
public:
  _HostSendOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _HostSendOpAdaptor(_HostSendOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getTensor();
  ::mlir::Value tensor();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _HostSendOp : public ::mlir::Op<_HostSendOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _HostSendOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("client_terminated"), ::llvm::StringRef("recv_device"), ::llvm::StringRef("send_device"), ::llvm::StringRef("send_device_incarnation"), ::llvm::StringRef("tensor_name")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getClientTerminatedAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getClientTerminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr client_terminatedAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr client_terminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getRecvDeviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getRecvDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr recv_deviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr recv_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSendDeviceAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSendDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr send_deviceAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr send_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getSendDeviceIncarnationAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getSendDeviceIncarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr send_device_incarnationAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr send_device_incarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getTensorNameAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getTensorNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr tensor_nameAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr tensor_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._HostSend");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getTensor();
  ::mlir::TypedValue<::mlir::TensorType> tensor();
  ::mlir::MutableOperandRange getTensorMutable();
  ::mlir::MutableOperandRange tensorMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setTensorNameAttr(::mlir::StringAttr attr);
  void setTensorName(::llvm::StringRef attrValue);
  void tensor_nameAttr(::mlir::StringAttr attr);
  void tensor_name(::llvm::StringRef attrValue);
  void setSendDeviceAttr(::mlir::StringAttr attr);
  void setSendDevice(::llvm::StringRef attrValue);
  void send_deviceAttr(::mlir::StringAttr attr);
  void send_device(::llvm::StringRef attrValue);
  void setSendDeviceIncarnationAttr(::mlir::IntegerAttr attr);
  void setSendDeviceIncarnation(uint64_t attrValue);
  void send_device_incarnationAttr(::mlir::IntegerAttr attr);
  void send_device_incarnation(uint64_t attrValue);
  void setRecvDeviceAttr(::mlir::StringAttr attr);
  void setRecvDevice(::llvm::StringRef attrValue);
  void recv_deviceAttr(::mlir::StringAttr attr);
  void recv_device(::llvm::StringRef attrValue);
  void setClientTerminatedAttr(::mlir::BoolAttr attr);
  void setClientTerminated(::llvm::Optional<bool> attrValue);
  void client_terminatedAttr(::mlir::BoolAttr attr);
  void client_terminated(::llvm::Optional<bool> attrValue);
  ::mlir::Attribute removeClient_terminatedAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 6 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_HostSendOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_InternalTestMustExecuteTrait_ declarations
//===----------------------------------------------------------------------===//

class _InternalTestMustExecuteTrait_Adaptor {
public:
  _InternalTestMustExecuteTrait_Adaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _InternalTestMustExecuteTrait_Adaptor(_InternalTestMustExecuteTrait_ op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _InternalTestMustExecuteTrait_ : public ::mlir::Op<_InternalTestMustExecuteTrait_, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _InternalTestMustExecuteTrait_Adaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._InternalTestMustExecuteTrait_");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_InternalTestMustExecuteTrait_)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_InternalTestNonResourceValueSideEffects_ declarations
//===----------------------------------------------------------------------===//

class _InternalTestNonResourceValueSideEffects_Adaptor {
public:
  _InternalTestNonResourceValueSideEffects_Adaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _InternalTestNonResourceValueSideEffects_Adaptor(_InternalTestNonResourceValueSideEffects_ op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getKey();
  ::mlir::Value key();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _InternalTestNonResourceValueSideEffects_ : public ::mlir::Op<_InternalTestNonResourceValueSideEffects_, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _InternalTestNonResourceValueSideEffects_Adaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._InternalTestNonResourceValueSideEffects_");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getKey();
  ::mlir::TypedValue<::mlir::TensorType> key();
  ::mlir::MutableOperandRange getKeyMutable();
  ::mlir::MutableOperandRange keyMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value key);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value key);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_InternalTestNonResourceValueSideEffects_)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_ListToArrayOp declarations
//===----------------------------------------------------------------------===//

class _ListToArrayOpAdaptor {
public:
  _ListToArrayOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _ListToArrayOpAdaptor(_ListToArrayOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInput();
  ::mlir::ValueRange input();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _ListToArrayOp : public ::mlir::Op<_ListToArrayOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _ListToArrayOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("N"), ::llvm::StringRef("T"), ::llvm::StringRef("Tin")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr NAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr NAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getTinAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getTinAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr TinAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr TinAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._ListToArray");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInput();
  ::mlir::Operation::operand_range input();
  ::mlir::MutableOperandRange getInputMutable();
  ::mlir::MutableOperandRange inputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getOutput();
  ::mlir::Operation::result_range output();
  mlir::OperandElementTypeRange getTin();
  mlir::OperandElementTypeRange Tin();
  size_t getN();
  size_t N();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_ListToArrayOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_RecvOp declarations
//===----------------------------------------------------------------------===//

class _RecvOpAdaptor {
public:
  _RecvOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _RecvOpAdaptor(_RecvOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _RecvOp : public ::mlir::Op<_RecvOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _RecvOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("client_terminated"), ::llvm::StringRef("recv_device"), ::llvm::StringRef("send_device"), ::llvm::StringRef("send_device_incarnation"), ::llvm::StringRef("tensor_name"), ::llvm::StringRef("tensor_type")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getClientTerminatedAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getClientTerminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr client_terminatedAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr client_terminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getRecvDeviceAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getRecvDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr recv_deviceAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr recv_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getSendDeviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getSendDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr send_deviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr send_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSendDeviceIncarnationAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSendDeviceIncarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr send_device_incarnationAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr send_device_incarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getTensorNameAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getTensorNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr tensor_nameAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr tensor_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getTensorTypeAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getTensorTypeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr tensor_typeAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr tensor_typeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._Recv");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getTensor();
  ::mlir::TypedValue<::mlir::TensorType> tensor();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::Type getTensorType();
  ::mlir::Type tensor_type();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setTensorNameAttr(::mlir::StringAttr attr);
  void setTensorName(::llvm::StringRef attrValue);
  void tensor_nameAttr(::mlir::StringAttr attr);
  void tensor_name(::llvm::StringRef attrValue);
  void setSendDeviceAttr(::mlir::StringAttr attr);
  void setSendDevice(::llvm::StringRef attrValue);
  void send_deviceAttr(::mlir::StringAttr attr);
  void send_device(::llvm::StringRef attrValue);
  void setSendDeviceIncarnationAttr(::mlir::IntegerAttr attr);
  void setSendDeviceIncarnation(uint64_t attrValue);
  void send_device_incarnationAttr(::mlir::IntegerAttr attr);
  void send_device_incarnation(uint64_t attrValue);
  void setRecvDeviceAttr(::mlir::StringAttr attr);
  void setRecvDevice(::llvm::StringRef attrValue);
  void recv_deviceAttr(::mlir::StringAttr attr);
  void recv_device(::llvm::StringRef attrValue);
  void setClientTerminatedAttr(::mlir::BoolAttr attr);
  void setClientTerminated(::llvm::Optional<bool> attrValue);
  void client_terminatedAttr(::mlir::BoolAttr attr);
  void client_terminated(::llvm::Optional<bool> attrValue);
  ::mlir::Attribute removeClient_terminatedAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 6 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_RecvOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_SendOp declarations
//===----------------------------------------------------------------------===//

class _SendOpAdaptor {
public:
  _SendOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _SendOpAdaptor(_SendOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getTensor();
  ::mlir::Value tensor();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _SendOp : public ::mlir::Op<_SendOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _SendOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("client_terminated"), ::llvm::StringRef("recv_device"), ::llvm::StringRef("send_device"), ::llvm::StringRef("send_device_incarnation"), ::llvm::StringRef("tensor_name")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getClientTerminatedAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getClientTerminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr client_terminatedAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr client_terminatedAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getRecvDeviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getRecvDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr recv_deviceAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr recv_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSendDeviceAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSendDeviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr send_deviceAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr send_deviceAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getSendDeviceIncarnationAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getSendDeviceIncarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr send_device_incarnationAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr send_device_incarnationAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr getTensorNameAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr getTensorNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  ::mlir::StringAttr tensor_nameAttrName() {
    return getAttributeNameForIndex(5);
  }

  static ::mlir::StringAttr tensor_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 5);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._Send");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getTensor();
  ::mlir::TypedValue<::mlir::TensorType> tensor();
  ::mlir::MutableOperandRange getTensorMutable();
  ::mlir::MutableOperandRange tensorMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::StringAttr getTensorNameAttr();
  ::llvm::StringRef getTensorName();
  ::mlir::StringAttr tensor_nameAttr();
  ::llvm::StringRef tensor_name();
  ::mlir::StringAttr getSendDeviceAttr();
  ::llvm::StringRef getSendDevice();
  ::mlir::StringAttr send_deviceAttr();
  ::llvm::StringRef send_device();
  ::mlir::IntegerAttr getSendDeviceIncarnationAttr();
  uint64_t getSendDeviceIncarnation();
  ::mlir::IntegerAttr send_device_incarnationAttr();
  uint64_t send_device_incarnation();
  ::mlir::StringAttr getRecvDeviceAttr();
  ::llvm::StringRef getRecvDevice();
  ::mlir::StringAttr recv_deviceAttr();
  ::llvm::StringRef recv_device();
  ::mlir::BoolAttr getClientTerminatedAttr();
  bool getClientTerminated();
  ::mlir::BoolAttr client_terminatedAttr();
  bool client_terminated();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setTensorNameAttr(::mlir::StringAttr attr);
  void setTensorName(::llvm::StringRef attrValue);
  void tensor_nameAttr(::mlir::StringAttr attr);
  void tensor_name(::llvm::StringRef attrValue);
  void setSendDeviceAttr(::mlir::StringAttr attr);
  void setSendDevice(::llvm::StringRef attrValue);
  void send_deviceAttr(::mlir::StringAttr attr);
  void send_device(::llvm::StringRef attrValue);
  void setSendDeviceIncarnationAttr(::mlir::IntegerAttr attr);
  void setSendDeviceIncarnation(uint64_t attrValue);
  void send_device_incarnationAttr(::mlir::IntegerAttr attr);
  void send_device_incarnation(uint64_t attrValue);
  void setRecvDeviceAttr(::mlir::StringAttr attr);
  void setRecvDevice(::llvm::StringRef attrValue);
  void recv_deviceAttr(::mlir::StringAttr attr);
  void recv_device(::llvm::StringRef attrValue);
  void setClientTerminatedAttr(::mlir::BoolAttr attr);
  void setClientTerminated(::llvm::Optional<bool> attrValue);
  void client_terminatedAttr(::mlir::BoolAttr attr);
  void client_terminated(::llvm::Optional<bool> attrValue);
  ::mlir::Attribute removeClient_terminatedAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value tensor, ::mlir::StringAttr tensor_name, ::mlir::StringAttr send_device, ::mlir::IntegerAttr send_device_incarnation, ::mlir::StringAttr recv_device, /*optional*/::mlir::BoolAttr client_terminated);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value tensor, ::llvm::StringRef tensor_name, ::llvm::StringRef send_device, uint64_t send_device_incarnation, ::llvm::StringRef recv_device, /*optional*/bool client_terminated = false);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 6 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_SendOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TPUCompileMlirOp declarations
//===----------------------------------------------------------------------===//

class _TPUCompileMlirOpAdaptor {
public:
  _TPUCompileMlirOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _TPUCompileMlirOpAdaptor(_TPUCompileMlirOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getDynamicShapes();
  ::mlir::ValueRange dynamic_shapes();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getMlirModuleAttr();
  ::llvm::StringRef getMlirModule();
  ::mlir::StringAttr mlir_moduleAttr();
  ::llvm::StringRef mlir_module();
  ::mlir::StringAttr getMetadataAttr();
  ::llvm::StringRef getMetadata();
  ::mlir::StringAttr metadataAttr();
  ::llvm::StringRef metadata();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _TPUCompileMlirOp : public ::mlir::Op<_TPUCompileMlirOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::AtLeastNResults<1>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpAsmOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _TPUCompileMlirOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("NumDynamicShapes"), ::llvm::StringRef("metadata"), ::llvm::StringRef("mlir_module"), ::llvm::StringRef("num_computations")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNumDynamicShapesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNumDynamicShapesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr NumDynamicShapesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr NumDynamicShapesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getMetadataAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getMetadataAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr metadataAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr metadataAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getMlirModuleAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getMlirModuleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr mlir_moduleAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr mlir_moduleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getNumComputationsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getNumComputationsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr num_computationsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr num_computationsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  void getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn);
  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._TPUCompileMlir");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getDynamicShapes();
  ::mlir::Operation::operand_range dynamic_shapes();
  ::mlir::MutableOperandRange getDynamicShapesMutable();
  ::mlir::MutableOperandRange dynamic_shapesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getCompilationStatus();
  ::mlir::TypedValue<::mlir::TensorType> compilation_status();
  ::mlir::Operation::result_range getProgram();
  ::mlir::Operation::result_range program();
  ::mlir::StringAttr getMlirModuleAttr();
  ::llvm::StringRef getMlirModule();
  ::mlir::StringAttr mlir_moduleAttr();
  ::llvm::StringRef mlir_module();
  ::mlir::StringAttr getMetadataAttr();
  ::llvm::StringRef getMetadata();
  ::mlir::StringAttr metadataAttr();
  ::llvm::StringRef metadata();
  size_t getNumDynamicShapes();
  size_t NumDynamicShapes();
  size_t getNumComputations();
  size_t num_computations();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setMlirModuleAttr(::mlir::StringAttr attr);
  void setMlirModule(::llvm::Optional<::llvm::StringRef> attrValue);
  void mlir_moduleAttr(::mlir::StringAttr attr);
  void mlir_module(::llvm::Optional<::llvm::StringRef> attrValue);
  void setMetadataAttr(::mlir::StringAttr attr);
  void setMetadata(::llvm::StringRef attrValue);
  void metadataAttr(::mlir::StringAttr attr);
  void metadata(::llvm::StringRef attrValue);
  ::mlir::Attribute removeMlir_moduleAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type compilation_status, ::mlir::TypeRange program, ::mlir::ValueRange dynamic_shapes, /*optional*/::mlir::StringAttr mlir_module, ::mlir::StringAttr metadata);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange dynamic_shapes, /*optional*/::mlir::StringAttr mlir_module, ::mlir::StringAttr metadata);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type compilation_status, ::mlir::TypeRange program, ::mlir::ValueRange dynamic_shapes, /*optional*/::llvm::StringRef mlir_module, ::llvm::StringRef metadata);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange dynamic_shapes, /*optional*/::llvm::StringRef mlir_module, ::llvm::StringRef metadata);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_TPUCompileMlirOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TPUCompileMlirPlaceholderProgramKeyOp declarations
//===----------------------------------------------------------------------===//

class _TPUCompileMlirPlaceholderProgramKeyOpAdaptor {
public:
  _TPUCompileMlirPlaceholderProgramKeyOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _TPUCompileMlirPlaceholderProgramKeyOpAdaptor(_TPUCompileMlirPlaceholderProgramKeyOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _TPUCompileMlirPlaceholderProgramKeyOp : public ::mlir::Op<_TPUCompileMlirPlaceholderProgramKeyOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _TPUCompileMlirPlaceholderProgramKeyOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._TPUCompileMlirPlaceholderProgramKey");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getProgram();
  ::mlir::TypedValue<::mlir::TensorType> program();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type program);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_TPUCompileMlirPlaceholderProgramKeyOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TPUDeviceOrdinalPlaceholderOp declarations
//===----------------------------------------------------------------------===//

class _TPUDeviceOrdinalPlaceholderOpAdaptor {
public:
  _TPUDeviceOrdinalPlaceholderOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _TPUDeviceOrdinalPlaceholderOpAdaptor(_TPUDeviceOrdinalPlaceholderOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _TPUDeviceOrdinalPlaceholderOp : public ::mlir::Op<_TPUDeviceOrdinalPlaceholderOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _TPUDeviceOrdinalPlaceholderOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._TPUDeviceOrdinalPlaceholder");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getDeviceOrdinal();
  ::mlir::TypedValue<::mlir::TensorType> device_ordinal();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type device_ordinal);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_TPUDeviceOrdinalPlaceholderOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_UnaryOpsCompositionOp declarations
//===----------------------------------------------------------------------===//

class _UnaryOpsCompositionOpAdaptor {
public:
  _UnaryOpsCompositionOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _UnaryOpsCompositionOpAdaptor(_UnaryOpsCompositionOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getX();
  ::mlir::Value x();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::ArrayAttr getOpNamesAttr();
  ::mlir::ArrayAttr getOpNames();
  ::mlir::ArrayAttr op_namesAttr();
  ::mlir::ArrayAttr op_names();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _UnaryOpsCompositionOp : public ::mlir::Op<_UnaryOpsCompositionOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::InferTypeOpInterface::Trait, ::mlir::InferShapedTypeOpInterface::Trait, ::mlir::OpTrait::InferTensorType, ::mlir::OpTrait::TF::SameOperandsAndResultTypeResolveRef, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _UnaryOpsCompositionOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("T"), ::llvm::StringRef("op_names")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getOpNamesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getOpNamesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr op_namesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr op_namesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._UnaryOpsComposition");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getX();
  ::mlir::TypedValue<::mlir::TensorType> x();
  ::mlir::MutableOperandRange getXMutable();
  ::mlir::MutableOperandRange xMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getY();
  ::mlir::TypedValue<::mlir::TensorType> y();
  ::mlir::ArrayAttr getOpNamesAttr();
  ::mlir::ArrayAttr getOpNames();
  ::mlir::ArrayAttr op_namesAttr();
  ::mlir::ArrayAttr op_names();
  ::mlir::Type getT();
  ::mlir::Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setOpNamesAttr(::mlir::ArrayAttr attr);
  void op_namesAttr(::mlir::ArrayAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type y, ::mlir::Value x, ::mlir::ArrayAttr op_names);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value x, ::mlir::ArrayAttr op_names);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value x, ::mlir::ArrayAttr op_names);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::LogicalResult inferReturnTypeComponents(::mlir::MLIRContext*context, ::llvm::Optional<::mlir::Location> location, ::mlir::ValueShapeRange operands, ::mlir::DictionaryAttr attributes, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::ShapedTypeComponents>&inferredReturnShapes);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      static bool isCompatibleReturnTypes(TypeRange inferred, TypeRange actual) {
        return ArraysAreCastCompatible(inferred, actual);
      }
    };
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_UnaryOpsCompositionOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_XlaHostComputeMlirOp declarations
//===----------------------------------------------------------------------===//

class _XlaHostComputeMlirOpAdaptor {
public:
  _XlaHostComputeMlirOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _XlaHostComputeMlirOpAdaptor(_XlaHostComputeMlirOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputs();
  ::mlir::ValueRange inputs();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getSendKeyAttr();
  ::llvm::StringRef getSendKey();
  ::mlir::StringAttr send_keyAttr();
  ::llvm::StringRef send_key();
  ::mlir::StringAttr getRecvKeyAttr();
  ::llvm::StringRef getRecvKey();
  ::mlir::StringAttr recv_keyAttr();
  ::llvm::StringRef recv_key();
  ::mlir::StringAttr getHostMlirModuleAttr();
  ::llvm::StringRef getHostMlirModule();
  ::mlir::StringAttr host_mlir_moduleAttr();
  ::llvm::StringRef host_mlir_module();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _XlaHostComputeMlirOp : public ::mlir::Op<_XlaHostComputeMlirOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _XlaHostComputeMlirOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("Tinputs"), ::llvm::StringRef("Toutputs"), ::llvm::StringRef("host_mlir_module"), ::llvm::StringRef("recv_key"), ::llvm::StringRef("send_key")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getToutputsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr ToutputsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr ToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getHostMlirModuleAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getHostMlirModuleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr host_mlir_moduleAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr host_mlir_moduleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getRecvKeyAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getRecvKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr recv_keyAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr recv_keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr getSendKeyAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr getSendKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  ::mlir::StringAttr send_keyAttrName() {
    return getAttributeNameForIndex(4);
  }

  static ::mlir::StringAttr send_keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 4);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._XlaHostComputeMlir");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputs();
  ::mlir::Operation::operand_range inputs();
  ::mlir::MutableOperandRange getInputsMutable();
  ::mlir::MutableOperandRange inputsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getOutputs();
  ::mlir::Operation::result_range outputs();
  ::mlir::StringAttr getSendKeyAttr();
  ::llvm::StringRef getSendKey();
  ::mlir::StringAttr send_keyAttr();
  ::llvm::StringRef send_key();
  ::mlir::StringAttr getRecvKeyAttr();
  ::llvm::StringRef getRecvKey();
  ::mlir::StringAttr recv_keyAttr();
  ::llvm::StringRef recv_key();
  ::mlir::StringAttr getHostMlirModuleAttr();
  ::llvm::StringRef getHostMlirModule();
  ::mlir::StringAttr host_mlir_moduleAttr();
  ::llvm::StringRef host_mlir_module();
  mlir::OperandElementTypeRange getTinputs();
  mlir::OperandElementTypeRange Tinputs();
  mlir::ResultElementTypeRange getToutputs();
  mlir::ResultElementTypeRange Toutputs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setSendKeyAttr(::mlir::StringAttr attr);
  void setSendKey(::llvm::StringRef attrValue);
  void send_keyAttr(::mlir::StringAttr attr);
  void send_key(::llvm::StringRef attrValue);
  void setRecvKeyAttr(::mlir::StringAttr attr);
  void setRecvKey(::llvm::StringRef attrValue);
  void recv_keyAttr(::mlir::StringAttr attr);
  void recv_key(::llvm::StringRef attrValue);
  void setHostMlirModuleAttr(::mlir::StringAttr attr);
  void setHostMlirModule(::llvm::Optional<::llvm::StringRef> attrValue);
  void host_mlir_moduleAttr(::mlir::StringAttr attr);
  void host_mlir_module(::llvm::Optional<::llvm::StringRef> attrValue);
  ::mlir::Attribute removeHost_mlir_moduleAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::ValueRange inputs, ::mlir::StringAttr send_key, ::mlir::StringAttr recv_key, /*optional*/::mlir::StringAttr host_mlir_module);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::ValueRange inputs, ::llvm::StringRef send_key, ::llvm::StringRef recv_key, /*optional*/::llvm::StringRef host_mlir_module = "");
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 5 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      func::FuncOp GetHostFunc(mlir::OwningOpRef<mlir::ModuleOp>* mlir_module);
    };
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_XlaHostComputeMlirOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_XlaRecvAtHostOp declarations
//===----------------------------------------------------------------------===//

class _XlaRecvAtHostOpAdaptor {
public:
  _XlaRecvAtHostOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _XlaRecvAtHostOpAdaptor(_XlaRecvAtHostOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getDynamicKey();
  ::mlir::Value dynamic_key();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::IntegerAttr getDeviceOrdinalAttr();
  uint64_t getDeviceOrdinal();
  ::mlir::IntegerAttr device_ordinalAttr();
  uint64_t device_ordinal();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _XlaRecvAtHostOp : public ::mlir::Op<_XlaRecvAtHostOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _XlaRecvAtHostOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("Toutputs"), ::llvm::StringRef("device_ordinal"), ::llvm::StringRef("key")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getToutputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr ToutputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr ToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getDeviceOrdinalAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getDeviceOrdinalAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr device_ordinalAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr device_ordinalAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getKeyAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr keyAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._XlaRecvAtHost");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getDynamicKey();
  ::mlir::TypedValue<::mlir::TensorType> dynamic_key();
  ::mlir::MutableOperandRange getDynamicKeyMutable();
  ::mlir::MutableOperandRange dynamic_keyMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getOutputs();
  ::mlir::Operation::result_range outputs();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::IntegerAttr getDeviceOrdinalAttr();
  uint64_t getDeviceOrdinal();
  ::mlir::IntegerAttr device_ordinalAttr();
  uint64_t device_ordinal();
  mlir::ResultElementTypeRange getToutputs();
  mlir::ResultElementTypeRange Toutputs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setKeyAttr(::mlir::StringAttr attr);
  void setKey(::llvm::StringRef attrValue);
  void keyAttr(::mlir::StringAttr attr);
  void key(::llvm::StringRef attrValue);
  void setDeviceOrdinalAttr(::mlir::IntegerAttr attr);
  void setDeviceOrdinal(uint64_t attrValue);
  void device_ordinalAttr(::mlir::IntegerAttr attr);
  void device_ordinal(uint64_t attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::Value dynamic_key, ::mlir::StringAttr key, ::mlir::IntegerAttr device_ordinal);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::Value dynamic_key, ::llvm::StringRef key, uint64_t device_ordinal);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_XlaRecvAtHostOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_XlaRecvAtHostV2Op declarations
//===----------------------------------------------------------------------===//

class _XlaRecvAtHostV2OpAdaptor {
public:
  _XlaRecvAtHostV2OpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _XlaRecvAtHostV2OpAdaptor(_XlaRecvAtHostV2Op op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getDynamicKey();
  ::mlir::Value dynamic_key();
  ::mlir::Value getDeviceOrdinal();
  ::mlir::Value device_ordinal();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _XlaRecvAtHostV2Op : public ::mlir::Op<_XlaRecvAtHostV2Op, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _XlaRecvAtHostV2OpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("Toutputs"), ::llvm::StringRef("key")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getToutputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr ToutputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr ToutputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getKeyAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr keyAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._XlaRecvAtHostV2");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getDynamicKey();
  ::mlir::TypedValue<::mlir::TensorType> dynamic_key();
  ::mlir::TypedValue<::mlir::TensorType> getDeviceOrdinal();
  ::mlir::TypedValue<::mlir::TensorType> device_ordinal();
  ::mlir::MutableOperandRange getDynamicKeyMutable();
  ::mlir::MutableOperandRange dynamic_keyMutable();
  ::mlir::MutableOperandRange getDeviceOrdinalMutable();
  ::mlir::MutableOperandRange device_ordinalMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getOutputs();
  ::mlir::Operation::result_range outputs();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  mlir::ResultElementTypeRange getToutputs();
  mlir::ResultElementTypeRange Toutputs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setKeyAttr(::mlir::StringAttr attr);
  void setKey(::llvm::StringRef attrValue);
  void keyAttr(::mlir::StringAttr attr);
  void key(::llvm::StringRef attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::mlir::StringAttr key);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange outputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::llvm::StringRef key);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_XlaRecvAtHostV2Op)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_XlaSendFromHostOp declarations
//===----------------------------------------------------------------------===//

class _XlaSendFromHostOpAdaptor {
public:
  _XlaSendFromHostOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _XlaSendFromHostOpAdaptor(_XlaSendFromHostOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputs();
  ::mlir::ValueRange inputs();
  ::mlir::Value getDynamicKey();
  ::mlir::Value dynamic_key();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::IntegerAttr getDeviceOrdinalAttr();
  uint64_t getDeviceOrdinal();
  ::mlir::IntegerAttr device_ordinalAttr();
  uint64_t device_ordinal();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _XlaSendFromHostOp : public ::mlir::Op<_XlaSendFromHostOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<1>::Impl, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _XlaSendFromHostOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("Tinputs"), ::llvm::StringRef("device_ordinal"), ::llvm::StringRef("key")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getDeviceOrdinalAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getDeviceOrdinalAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr device_ordinalAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr device_ordinalAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getKeyAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr keyAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._XlaSendFromHost");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputs();
  ::mlir::Operation::operand_range inputs();
  ::mlir::TypedValue<::mlir::TensorType> getDynamicKey();
  ::mlir::TypedValue<::mlir::TensorType> dynamic_key();
  ::mlir::MutableOperandRange getInputsMutable();
  ::mlir::MutableOperandRange inputsMutable();
  ::mlir::MutableOperandRange getDynamicKeyMutable();
  ::mlir::MutableOperandRange dynamic_keyMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::IntegerAttr getDeviceOrdinalAttr();
  uint64_t getDeviceOrdinal();
  ::mlir::IntegerAttr device_ordinalAttr();
  uint64_t device_ordinal();
  mlir::OperandElementTypeRange getTinputs();
  mlir::OperandElementTypeRange Tinputs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setKeyAttr(::mlir::StringAttr attr);
  void setKey(::llvm::StringRef attrValue);
  void keyAttr(::mlir::StringAttr attr);
  void key(::llvm::StringRef attrValue);
  void setDeviceOrdinalAttr(::mlir::IntegerAttr attr);
  void setDeviceOrdinal(uint64_t attrValue);
  void device_ordinalAttr(::mlir::IntegerAttr attr);
  void device_ordinal(uint64_t attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::StringAttr key, ::mlir::IntegerAttr device_ordinal);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::StringAttr key, ::mlir::IntegerAttr device_ordinal);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::llvm::StringRef key, uint64_t device_ordinal);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::llvm::StringRef key, uint64_t device_ordinal);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_XlaSendFromHostOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_XlaSendFromHostV2Op declarations
//===----------------------------------------------------------------------===//

class _XlaSendFromHostV2OpAdaptor {
public:
  _XlaSendFromHostV2OpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  _XlaSendFromHostV2OpAdaptor(_XlaSendFromHostV2Op op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputs();
  ::mlir::ValueRange inputs();
  ::mlir::Value getDynamicKey();
  ::mlir::Value dynamic_key();
  ::mlir::Value getDeviceOrdinal();
  ::mlir::Value device_ordinal();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class _XlaSendFromHostV2Op : public ::mlir::Op<_XlaSendFromHostV2Op, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, GetResourceInstanceInterface::Trait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _XlaSendFromHostV2OpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("Tinputs"), ::llvm::StringRef("key")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getTinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getTinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr TinputsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr TinputsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getKeyAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getKeyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr keyAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr keyAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._XlaSendFromHostV2");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputs();
  ::mlir::Operation::operand_range inputs();
  ::mlir::TypedValue<::mlir::TensorType> getDynamicKey();
  ::mlir::TypedValue<::mlir::TensorType> dynamic_key();
  ::mlir::TypedValue<::mlir::TensorType> getDeviceOrdinal();
  ::mlir::TypedValue<::mlir::TensorType> device_ordinal();
  ::mlir::MutableOperandRange getInputsMutable();
  ::mlir::MutableOperandRange inputsMutable();
  ::mlir::MutableOperandRange getDynamicKeyMutable();
  ::mlir::MutableOperandRange dynamic_keyMutable();
  ::mlir::MutableOperandRange getDeviceOrdinalMutable();
  ::mlir::MutableOperandRange device_ordinalMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::StringAttr getKeyAttr();
  ::llvm::StringRef getKey();
  ::mlir::StringAttr keyAttr();
  ::llvm::StringRef key();
  mlir::OperandElementTypeRange getTinputs();
  mlir::OperandElementTypeRange Tinputs();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void setKeyAttr(::mlir::StringAttr attr);
  void setKey(::llvm::StringRef attrValue);
  void keyAttr(::mlir::StringAttr attr);
  void key(::llvm::StringRef attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::mlir::StringAttr key);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::mlir::StringAttr key);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::llvm::StringRef key);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange inputs, ::mlir::Value dynamic_key, ::mlir::Value device_ordinal, ::llvm::StringRef key);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  std::string GetResourceInstanceStr();
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace TF
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::TF::_XlaSendFromHostV2Op)


#endif  // GET_OP_CLASSES

